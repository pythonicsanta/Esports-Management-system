from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from users.models import User
from blog.models import Slot,Post,Participants
from . import Checksum
from django.contrib import messages



from paytm.models import PaytmHistory
# Create your views here.


def home(request):
    return HttpResponse("<html><p>Welcome " + request.user.username + "</p><a href='" + settings.HOST_URL + "/paytm/payment'>PayNow</html>")

@login_required
def payment(request,order_id):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    #order_id = Checksum.__id_generator__()
    order_id=order_id
    dec=order_id.split('O')
    if dec[0] and dec[1]:
        post_id=int(dec[0])
        player_id=int(dec[1])
    else:
        post_id,player_id=0,0

    user=get_object_or_404(User,pk=player_id)
    post=get_object_or_404(Post,pk=post_id)
    bill_amount = post.entry_fee
    if bill_amount:
        data_dict = {
            'MID': MERCHANT_ID,
            'ORDER_ID': str(order_id),
            'TXN_AMOUNT': str(bill_amount),
            'CUST_ID': 'nagillaxman@gmail.com',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': settings.PAYTM_WEBSITE,
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': CALLBACK_URL,
        }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request, "paytm/payment.html", {'paytmdict': param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


'''
@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            print('verified')
            for key in request.POST:
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            #PaytmHistory.objects.create(user=settings.USER, **data_dict)
            return render(request, "paytm/response.html", {"paytm": data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

'''
@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            if data_dict['RESPCODE'] == '01':
                print('order successful')
                order_id=data_dict['ORDERID']
                dec=order_id.split('O')
                post_id=int(dec[0])
                player_id=int(dec[1])
                order=Participants.objects.get(player_id=player_id,post_id=post_id).order_id
                if str(order)==str(order_id):
                    user=User.objects.get(id=player_id)
                    post=Post.objects.get(id=post_id)
                    participant=Participants.objects.get(player_id=player_id)
                    match=post.match_type
                    PaytmHistory.objects.create(user=user, **data_dict)
                    Slot.objects.create(post_id=post,player_id=user,players=participant,match=match,order_id=order_id)

                #print("post ",post_id," player ",player_id)
                return render(request,"paytm/response.html",{"paytm":order_id})

            else:
                print('order was not successful because' + datadict_dict['RESPMSG'])


        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
