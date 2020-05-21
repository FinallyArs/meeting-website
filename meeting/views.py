from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.shortcuts import reverse
from .forms import RegistrationForm, ProfileForm, MessageForm
from .models import Profile, Chat
from .forms import ContactForm
from django.core.mail import send_mail


class UserListView(ListView):
    queryset = Profile.objects.all()
    context_object_name = 'users'
    paginate_by = 12
    template_name = 'users_list.html'


@login_required
def user_details(request, pk):
    user = get_object_or_404(Profile, pk=pk)
    is_liked = False
    if user.likes.filter(id=request.user.id).exists():
        is_liked = True
    if user.birth_date is None:
        return render(request, 'user_details.html', context={
            'user': user,
            'is_liked': is_liked,
            'total_likes': user.total_likes(),
            'get_online_info': user.get_online_info(),
            'is_online': user.is_online()})
    return render(request, 'user_details.html', context={
        'user': user, 'is_liked': is_liked,
        'total_likes': user.total_likes(),
        'age': user.age(),
        'get_online_info': user.get_online_info(),
        'is_online': user.is_online()
    })


def like_profile(request):
    user = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    is_liked = False
    if user.likes.filter(id=request.user.id).exists():
        user.likes.remove(request.user)
        is_liked = False
    else:
        user.likes.add(request.user)
        messages.success(request, u"You liked the user !")
        is_liked = True
    return redirect('user_detail', pk=user.pk)


class HomeView(TemplateView):
    template_name = "home.html"


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('edit_profile')

    def form_valid(self, form):
        form.save()
        user = authenticate(self.request,
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1']
                            )
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect(reverse("edit_profile"))
        if request.user.profile.birth_date is None:
            context = {
                'selected_user': request.user,
                'is_online': request.user.profile.is_online(),
                'get_online_info': request.user.profile.get_online_info()
            }
            return render(request, self.template_name, context)

        context = {
            'selected_user': request.user,
            'age': request.user.profile.age(),
            'is_online': request.user.profile.is_online(),
            'get_online_info': request.user.profile.get_online_info(),

        }
        return render(request, self.template_name, context)


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES,
                               instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Profile has been updated!!")
                return redirect(reverse("list"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.profile.id])
        return render(request, 'dialogs.html', {'user_profile': request.user,
                                                'chats': chats})


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user.profile in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(
                    author=request.user.profile).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'messages.html',
            {
                'user_profile': request.user.profile,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user.profile
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        user = get_object_or_404(Profile, id=user_id)
        chats = Chat.objects.filter(
            members__in=[request.user.profile, user_id],
            type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if user.likes.filter(id=request.user.id).exists() \
                and request.user.profile.likes.filter(id=user_id).exists() \
                and chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user.profile)
            chat.members.add(user_id)
        else:
            chat = Chat.objects.create()
            chat.members.add(request.user.profile)
            chat.members.add(user_id)
        if not user.likes.filter(id=request.user.id).exists() \
                and request.user.profile.likes.filter(id=user_id).exists():
            messages.error(
                request,
                u"Impossible to start chat. This user hasn't liked you yet.")
            return redirect('user_detail', pk=user.pk)
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))


def contactform(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recepients = ['finallyars99@gmail.com']
            if copy:
                recepients.append(sender)
            try:
                send_mail(subject,
                          message,
                          'finallyars99@gmail.com',
                          recepients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponseRedirect('thanks')

    else:
        form = ContactForm()
    return render(request,
                  'contacts.html',
                  {'form': form,
                   'username': auth.get_user(request).username})


def thanks(request):
    thanks = 'thanks'
    return render(request, 'registration/thanks.html', {'thanks': thanks})
