from django.shortcuts import render, get_object_or_404, redirect


def statutes(request):
    return render(request, 'youth_org/statutes.html')

def sovereign_youth(request):
    return render(request, 'youth_org/sovereign_youth.html')

def programm(request):
    return render(request, 'youth_org/programm.html')

def board(request):
    # Sample board member data - you can replace this with data from your database
    board_members = [
        {
            'name': 'Max Mustermann',
            'position': '1. Vorsitzender',
            'image': 'placeholder-user.jpg',  # Replace with actual image path
            'bio': 'Verantwortlich für die strategische Ausrichtung und Führung des Vereins.'
        },
        {
            'name': 'Erika Musterfrau',
            'position': '2. Vorsitzende',
            'image': 'placeholder-user.jpg',
            'bio': 'Unterstützt die Vereinsführung und übernimmt Vertretungsaufgaben.'
        },
        {
            'name': 'Thomas Test',
            'position': 'Schatzmeister',
            'image': 'placeholder-user.jpg',
            'bio': 'Verantwortlich für die Finanzen und die wirtschaftliche Stabilität des Vereins.'
        },
        {
            'name': 'Anna Beispiel',
            'position': 'Schriftführerin',
            'image': 'placeholder-user.jpg',
            'bio': 'Zuständig für Protokolle und die Dokumentation der Vereinsaktivitäten.'
        },
    ]
    return render(request, 'youth_org/board.html', {'board_members': board_members})
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import ForumMessage, YouthOrganization, YouthMember
from .forms import YouthOrganizationForm, YouthMemberForm

def home(request):
    # Board members data
    board_members = [
        {
            'name': 'Max Mustermann',
            'position': '1. Vorsitzender',
            'image': 'placeholder-user.jpg',
            'bio': 'Verantwortlich für die strategische Ausrichtung und Führung des Vereins.'
        },
        {
            'name': 'Erika Musterfrau',
            'position': '2. Vorsitzende',
            'image': 'placeholder-user.jpg',
            'bio': 'Unterstützt die Vereinsführung und übernimmt Vertretungsaufgaben.'
        },
        {
            'name': 'Thomas Test',
            'position': 'Schatzmeister',
            'image': 'placeholder-user.jpg',
            'bio': 'Verantwortlich für die Finanzen und die wirtschaftliche Stabilität des Vereins.'
        },
        {
            'name': 'Anna Beispiel',
            'position': 'Schriftführerin',
            'image': 'placeholder-user.jpg',
            'bio': 'Zuständig für Protokolle und die Dokumentation der Vereinsaktivitäten.'
        },
    ]
    return render(request, 'home.html', {'board_members': board_members})

class YouthOrganizationListView(ListView):
    model = YouthOrganization
    template_name = 'youth_org/organization_list.html'
    context_object_name = 'organizations'
    paginate_by = 10
    
    def get_queryset(self):
        return YouthOrganization.objects.filter(is_active=True).order_by('name')

class YouthOrganizationDetailView(DetailView):
    model = YouthOrganization
    template_name = 'youth_org/organization_detail.html'
    context_object_name = 'organization'

class YouthOrganizationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = YouthOrganization
    form_class = YouthOrganizationForm
    template_name = 'youth_org/organization_form.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Organization created successfully!')
        return super().form_valid(form)

class YouthOrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = YouthOrganization
    form_class = YouthOrganizationForm
    template_name = 'youth_org/organization_form.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Organization updated successfully!')
        return super().form_valid(form)

class YouthMemberCreateView(LoginRequiredMixin, CreateView):
    model = YouthMember
    form_class = YouthMemberForm
    template_name = 'youth_org/member_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Successfully joined the youth organization!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('youth-organization-detail', kwargs={'pk': self.object.organization.pk})

class YouthMemberUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = YouthMember
    form_class = YouthMemberForm
    template_name = 'youth_org/member_form.html'
    
    def test_func(self):
        member = self.get_object()
        return self.request.user == member.user or self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('youth-organization-detail', kwargs={'pk': self.object.organization.pk})

@login_required
def youth_dashboard(request):
    try:
        member = request.user.youth_profile
        organization = member.organization
        context = {
            'member': member,
            'organization': organization,
            'upcoming_events': [],  # You can add events functionality later
        }
        return render(request, 'youth_org/dashboard.html', context)
    except YouthMember.DoesNotExist:
        organizations = YouthOrganization.objects.filter(is_active=True)
        return render(request, 'youth_org/join_organization.html', {'organizations': organizations})

@login_required(login_url='/login/')
def member(request):
    channel = request.GET.get('channel', 'general')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ForumMessage.objects.create(
                author=request.user,
                channel=channel,
                content=content,
                timestamp=timezone.now()
            )
            return redirect(f'/member/?channel={channel}')
    messages = ForumMessage.objects.filter(channel=channel).order_by('timestamp')
    channels = [
        ('general', 'Allgemein'),
        ('projects', 'Projekte'),
        ('offtopic', 'Off-Topic'),
    ]
    return render(request, 'member.html', {
        'messages': messages,
        'channels': channels,
        'current_channel': channel,
    })
