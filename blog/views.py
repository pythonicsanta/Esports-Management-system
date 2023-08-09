from random import randint
from django.http import Http404
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib import messages
from . forms import ResultImageForm
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView,
        )
from . models import Post,Slot,Participants,Result
from users.models import User
from datetime import datetime

# paytm imports

#reception

# Create your views here.

def home(request):
    if request.user.is_organizer == True:
        print('bhai ho gya')
    else:
        print(':(')
    content={'posts':Post.objects.all()}
    return render(request,'blog/home.html',content)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'         # default template format <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering = ['-match_date']

class PostDetailView(DetailView):
    model = Post                          # default template format <app>/<model>_<viewtype>.html
                                          # we created template      blog/post_detail.html
                                          #and change model name with object, as for post model,> name it as object
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        pk=self.kwargs['pk']
        post=Post.objects.get(pk=pk)
        match=post.match_type
        match_date=post.match_date
        print(match_date)
        match_date=match_date.strftime('%Y-%m-%d %H:%M')
        time = datetime.now()
        time=time.strftime('%Y-%m-%d %H:%M')
        if str(match_date) > str(time):
            status=True
            #print(match_date,time,'True')
        else:
            status=False
            #print(match_date,time,'False')

        count=(Slot.objects.filter(post_id=pk).count())
        count=int(count)
        total_seats=int(post.num_seats)
        total_sum=count*int(post.entry_fee)
        results=(Result.objects.filter(post_id=pk))
        context['total_seats']=total_seats
        context['total_sum']=total_sum
        context['count'] =count
        context['status'] =status
        context['results'] = results
        return context
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title','match_date','match_type','entry_fee','per_kill','prize','num_seats','description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_organizer == True :
            return True
        else:
            return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','match_date','match_type','entry_fee','per_kill','prize','num_seats','description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user.is_staff == True:
            return True
        elif self.request.user == post.author and self.request.user.is_organizer == True:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
            post=self.get_object()
            if self.request.user.is_staff == True:
                return True
            elif self.request.user == post.author and self.request.user.is_organizer == True:
                return True
            else:
                return False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff == True:
            status=True
            context['status'] =status
            return context
        else:

            pk=self.kwargs['pk']
            post=Post.objects.get(pk=pk)
            match_date=post.match_date
            match_date=match_date.strftime('%Y-%m-%d %H')
            time = datetime.now()
            time=time.strftime('%Y-%m-%d %H')
            if str(match_date) < str(time):
                status=True
                #print(match_date,time,'True')
            else:
                status=False
                #print(match_date,time,'False')
            context['status'] =status
            return context

def ifregistered(request,pk):
    try:
        usr=request.user.id
        slot=Slot.objects.get(post_id=pk,player_id=usr)
        if slot.count() > 1:
            print('gadbad h bhai kuch to ')
            return False
        else:
            print('all ok ')
            return True
    except Slot.DoseNotExist:
        return False
    except:
        return False
        #messages.info(request, "You can register")



@login_required
def slot_book(request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    usr=request.user.id
    match_date=post.match_date
    match_date=match_date.strftime('%Y-%m-%d %H:%M')
    time = datetime.now()
    time=time.strftime('%Y-%m-%d %H:%M')

    if str(match_date) > str(time):status=True
    else:
        return redirect(post)
    try:
        slot=Slot.objects.get(post_id=pk,player_id=usr)
        messages.warning(request, "You are already registered")
        return redirect(post)
    except:
        if post.author.id == request.user.id:
            messages.warning(request, "Organizer cannot registered")
            return redirect(post)
        #messages.info(request, "You can register")

    if request.method == 'POST':
        player = request.user
        #print('ye raha player ',player,' ok!')
        match = post.match_type
        mobilenumber = request.POST['phone']
        #print(mobilenumber)
        p1=request.POST['player1']
        p2=request.POST['player2']
        p3=request.POST['player3']
        p4=request.POST['player4']
        order_id=str(pk)+'O'+str(usr)+'O'+ str(randint(1,2000))+'PUBG'
        try:
            p=Participants.objects.get(post_id=pk,player_id=usr)
            print("Bhai wapis ki krra === chal thik h leleta tko koi dikkat ayi hogi")
            p.mobilenumber=mobilenumber
            p.player1,p.player2,p.player3,p.player4=p1,p2,p3,p4
            p.order_id=order_id
            p.save()
            print(p)
        except:
            obj = Participants(post_id=post,player_id=player,mobilenumber=mobilenumber,player1=p1,player2=p2,player3=p3,player4=p4)
            obj.order_id=order_id
            obj.save()


        print('order id bn gyi dekh ',order_id)
        messages.success(request,f'Your have register Successfully!')
        return redirect('payment',order_id)

    else:
        raise Http404


def match_result(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        if selfsecurity(request,pk):
            post = Post.objects.get(pk=pk)
            usr=request.user.id
            match_date=post.match_date
            match_date=match_date.strftime('%Y-%m-%d %H:%M')
            time = datetime.now()
            time=time.strftime('%Y-%m-%d %H:%M')

            if str(match_date) < str(time):
                status=True
                results=Slot.objects.filter(post_id=pk)
                if request.method == 'POST':
                    #print('post m ghus gae bhai')
                    kills=','.join(request.POST.getlist('kills'))

                    kills=kills.split(',')

                    for result,kill in zip( results, kills):
                        print(result,kill,'>')
                        if not kill:
                            kill=0
                        result.players.kills=kill
                        result.save()
                    messages.success(request, 'Results Updated Successfully.')
                    return redirect('post-detail',pk)
                else:

                    context={
                        'results':results
                    }
                return render(request,'blog/result.html',context)
            else:
                messages.success(request,'Result can be uploaded after match finishes')
                return redirect(post)


        else:
            raise Http404
    else:
        raise Http404

def match_result_images(request,pk):
    if request.user.is_authenticated:
        if selfsecurity(request,pk):
            post = Post.objects.get(pk=pk)
            usr=request.user.id
            match_date=post.match_date
            match_date=match_date.strftime('%Y-%m-%d %H:%M')
            time = datetime.now()
            time=time.strftime('%Y-%m-%d %H:%M')

            if str(match_date) < str(time):
                status=True
                ResultImageFormSet = modelformset_factory(Result,form=ResultImageForm,extra=10)
                if request.method == 'POST':
                    formset = ResultImageFormSet(request.POST,request.FILES,queryset=Result.objects.none())
                    if formset.is_valid():
                        for form in formset.cleaned_data:
                            if form:
                                image = form['image']
                                post=Post.objects.get(pk=pk)
                                photo = Result(post_id=post, image=image)
                                photo.save()
                        messages.success(request,'Result Uploaded Successfully')
                        return redirect(post)
                    else:
                        print('error h kuch to')
                else:
                    formset = ResultImageFormSet(queryset=Result.objects.none())
                return render(request,'blog/result_images.html',{'formset':formset})

            else:
                messages.success(request,'Result can be uploaded after match finishes')
                return redirect(post)


        else:
            raise Http404
    else:
        raise Http404

def view_regeistered(request,pk):
    if request.user.is_authenticated:
        if selfsecurity(request,pk):
            results=Slot.objects.filter(post_id=pk)
            context={
                'results':results
            }
            context['page']=pk
            return render(request,'blog/view_registerations.html',context)

        else:
            raise Http404
    else:
        raise Http404

def room_details(request,pk):
    if request.user.is_authenticated:
        print('han andr bhej die h kam ka bnda kehke ')
        if selfsecurity(request,pk):
            print('staff hu m ')
            if request.method == 'POST':
                room=Post.objects.get(id=pk)
                room.room_details=request.POST['room']
                room.save()
                print('han save kr die hai ')
                messages.success(request, "Room Details Posted")
                return redirect('blog-home')
            else:
                return redirect('blog-home')
        else:raise Http404
    else:
        raise Http404


#custom security checks
def selfsecurity(request,post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_staff == True:
        return True
    elif request.user == post.author and request.user.is_organizer == True:
        return True
    else:
        return False

def about(request):

    return render(request,'blog/about.html')
