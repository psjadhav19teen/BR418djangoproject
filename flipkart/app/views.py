from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    UserProfile,
    Categories,
    SubCategories,
    Products,
    Carts,
    Orders,
    Payments,
    Country,
    City,
    Wishlist,
    Address,
)
from django.contrib.auth.models import User

# Create your views here.


def index(req):
    allproducts = Products.objects.all()
    print(allproducts)
    allcategories = Categories.objects.all()
    print(allcategories)
    return render(
        req, "index.html", {"allproducts": allproducts, "allcategories": allcategories}
    )


from django.core.exceptions import ValidationError


def validate_password(password):
    if len(password) < 8 or len(password) > 128:
        raise ValidationError(
            "Password must be atleast 8 character long and less than 128"
        )

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    specialchars = "@$!%*?&"

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in specialchars:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter")

    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter")

    if not has_digit:
        raise ValidationError("Password must contain at least one digit letter")

    if not has_special:
        raise ValidationError(
            "Password must contain at least one special char (e.g. @$!%*?&)"
        )

    commonpassword = ["password", "123456", "qwerty", "abc123"]
    if password in commonpassword:
        raise ValidationError("This password is too common. Please choose another one.")


def signup(req):
    if req.method == "GET":
        print(req.method)  # GET
        return render(req, "signup.html")
    else:
        print(req.method)  # POST
        uname = req.POST["uname"]
        uemail = req.POST["uemail"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        print(uname, upass, ucpass, uemail)
        context = {}
        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "signup.html", context)

        if upass != ucpass:
            errmsg = "Password and Confirm password must be same"
            context = {"errmsg": errmsg}
            return render(req, "signup.html", context)
        elif uname == upass:
            errmsg = "Password should not be same as email id"
            context = {"errmsg": errmsg}
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(
                    username=uname, email=uemail, password=upass
                )
                userdata.set_password(upass)
                userdata.save()
                print(User.objects.all())
                return redirect("signin")
            except:
                errmsg = "User already exists. Try with different username"
                context = {"errmsg": errmsg}
                return render(req, "signup.html", context)


from django.contrib.auth import authenticate, login, logout


def signin(req):
    if req.method == "GET":
        print(req.method)
        return render(req, "signin.html")
    else:
        uname = req.POST.get("uname")
        uemail = req.POST.get("uemail")
        upass = req.POST["upass"]
        print(uname, uemail, upass)
        # userdata = User.objects.filter(email=uemail, password=upass)
        userdata = authenticate(username=uname, email=uemail, password=upass)
        print(userdata)  # if matched with user then it show its id
        if userdata is not None:
            login(req, userdata)
            # return render(req, "dashboard.html")
            return redirect("/")
        else:
            context = {}
            context["errmsg"] = "Invalid email or password"
            return render(req, "signin.html", context)


def userlogout(req):
    logout(req)
    return redirect("/")


from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages


def req_password(req):
    if req.method == "POST":
        uemail = req.POST["uemail"]
        try:
            user = User.objects.get(email=uemail)
            print(user.email, user)

            userotp = random.randint(1111, 999999)
            req.session["otp"] = userotp  # store otp into session

            subject = "PetStore- OTP for Reset Password"
            msg = f"Hello {user}\n Your OTP to reset password is:{userotp}\n Thank You for using our services."
            emailfrom = settings.EMAIL_HOST_USER
            receiver = [user.email]
            send_mail(subject, msg, emailfrom, receiver)

            return redirect("reset_password", uemail=user.email)

        except User.DoesNotExist:
            messages.error(req, "No account found with this email id.")
            return render(req, "req_password.html")
    else:
        return render(req, "req_password.html")


def reset_password(req, uemail):
    user = User.objects.get(email=uemail)
    print(user)
    if req.method == "POST":
        otp_entered = req.POST["otp"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        userotp = req.session.get("otp")
        print(userotp, type(userotp))
        print(otp_entered, type(otp_entered), upass, ucpass)

        if int(otp_entered) != int(userotp):
            messages.error(req, "OTP does not match! Try Again.")
            return render(req, "reset_password.html", {"uemail": uemail})

        elif upass != ucpass:
            messages.error(req, "Confirm password and password do not match.")
            return render(req, "reset_password.html", {"uemail": uemail})

        else:
            try:
                validate_password(upass)
                user.set_password(upass)
                user.save()
                return redirect("signin")
            except ValidationError as e:
                messages.error(req, str(e))
                return render(req, "reset_password.html", {"uemail": uemail})
    else:
        return render(req, "reset_password.html", {"uemail": uemail})


def about(req):
    return render(req, "about.html")


def contact(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        umobile = req.POST["umobile"]
        uemail = req.POST["uemail"]
        msg = req.POST["msg"]
        print(uname, umobile, uemail, msg)

        subject = "My Query"
        msg = f"Hello Team, {msg}."
        emailfrom = settings.EMAIL_HOST_USER
        receiver = [uemail]
        send_mail(subject, msg, emailfrom, receiver)

        return redirect("/")
    else:
        return render(req, "contact.html")


from django.contrib import messages
from django.db.models import Q


def searchproduct(req):
    query = req.GET["q"]
    if query:
        allproducts = Products.objects.filter(
            Q(productname__icontains=query) | Q(description__icontains=query)
        )
        if len(allproducts) == 0:
            messages.error(req, "No result found!!")
    else:
        allproducts = Products.objects.all()

    context = {"allproducts": allproducts}
    return render(req, "index.html", context)


def electronics_search(req):
    if req.method == "GET":
        # ele_category = Categories.objects.filter(name="Electronics").first()
        # ele_category = Categories.objects.get(name="Electronics")  # (=) for single row
        # print("ele=", ele_category)
        # allproducts = Products.objects.filter(categories=ele_category)  # many rows
        # print("all ele=", allproducts)

        allproducts = Products.productmanager.electronics_list()
        print(allproducts)

        if len(allproducts) == 0:
            messages.error(req, "No result found!")

        allcategories = Categories.objects.all()
        print(allcategories)
        context = {"allproducts": allproducts, "allcategories": allcategories}
        return render(req, "index.html", context)


def cloths_search(req):
    if req.method == "GET":
        allproducts = Products.productmanager.cloths_list()
        print(allproducts)

        if len(allproducts) == 0:
            messages.error(req, "No result found!")

        allcategories = Categories.objects.all()
        print(allcategories)
        context = {"allproducts": allproducts, "allcategories": allcategories}
        return render(req, "index.html", context)


def shoes_search(req):
    if req.method == "GET":
        allproducts = Products.productmanager.shoes_list()
        print(allproducts)

        if len(allproducts) == 0:
            messages.error(req, "No result found!")

        allcategories = Categories.objects.all()
        print(allcategories)
        context = {"allproducts": allproducts, "allcategories": allcategories}
        return render(req, "index.html", context)


def serchby_pricerange(req):
    if req.method == "GET":
        return render(req, "index.html")
    else:
        r1 = req.POST["min"]
        r2 = req.POST["max"]
        print(r1, r2)
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts = Products.productmanager.pricerange(r1, r2)
            # allproducts=Products.objects.filter(price__range=(r1,r2))
            allcategories = Categories.objects.all()
            print(allcategories)
            if len(allproducts) == 0:
                messages.error(req, "No result found!")
            context = {"allproducts": allproducts, "allcategories": allcategories}
            return render(req, "index.html", context)
        else:
            allproducts = Products.objects.all()
            allcategories = Categories.objects.all()
            context = {"allproducts": allproducts, "allcategories": allcategories}
            return render(req, "index.html", context)


def productdetails(req, productid):
    product = Products.objects.get(productid=productid)
    context = {"product": product}
    return render(req, "productdetails.html", context)


from django.utils import timezone
from datetime import timedelta


def showcarts(req):
    username = req.user
    allcarts = Carts.objects.filter(userid=username.id)

    totalitems = allcarts.count()
    totalamount = sum(x.productid.price * x.qty for x in allcarts)

    has_profile = UserProfile.objects.filter(userid=username).exists()
    has_address = Address.objects.filter(userid=username).exists()

    estimated_delivery = timezone.now().date() + timedelta(days=5)

    context = {
        "allcarts": allcarts,
        "username": username,
        "totalitems": totalitems,
        "totalamount": totalamount,
        "has_profile": has_profile,
        "has_address": has_address,
        "date": estimated_delivery,
    }

    return render(req, "showcarts.html", context)


def addtocart(req, productid):
    if req.user.is_authenticated:
        userid = req.user
    else:
        userid = None  # optionally handle guest cart differently

    product = get_object_or_404(Products, productid=productid)

    # Try to get the cart item for the user & product
    cartitem, created = Carts.objects.get_or_create(userid=userid, productid=product)

    # Determine the new quantity we're trying to set
    new_qty = cartitem.qty + 1 if not created else 1

    # Check if requested quantity exceeds stock
    if new_qty > product.quantity_available:
        messages.error(req, "Cannot add more items — only limited stock available.")
        return redirect("/showcarts")

    # Update or create cart item
    cartitem.qty = new_qty
    cartitem.save()
    return redirect("/showcarts")


def removecart(req, productid):
    if req.user.is_authenticated:
        userid = req.user
    else:
        userid = None

    cartitems = Carts.objects.get(productid=productid, userid=userid)
    cartitems.delete()
    return redirect("/showcarts")


def updateqty(req, qv, productid):
    product = get_object_or_404(Products, productid=productid)
    allcarts = Carts.objects.filter(productid=productid, userid=req.user)

    if not allcarts.exists():
        messages.error(req, "Item not found in cart.")
        return redirect("/showcarts")

    cart_item = allcarts.first()

    if qv == 1:
        # Check if there's enough quantity available in product
        if cart_item.qty < product.quantity_available:
            cart_item.qty += 1
            cart_item.save()
        else:
            messages.warning(req, "Only limited stock available.")
    else:
        # Decrease quantity or remove item from cart
        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("/showcarts")


def checkout_single(request, productid):
    user = request.user

    try:
        cart_item = Carts.objects.get(userid=user, productid__productid=productid)
    except Carts.DoesNotExist:
        messages.error(request, "Product not found in your cart.")
        return redirect("/showcarts")

    address = Address.objects.filter(userid=user)
    if not address.exists():
        messages.warning(request, "Please add an address before checking out.")
        return redirect("/addaddress")

    cart_data = [
        {
            "productname": cart_item.productid.productname,
            "qty": cart_item.qty,
            "price": cart_item.productid.price,
            "subtotal": cart_item.qty * cart_item.productid.price,
        }
    ]
    total = cart_data[0]["subtotal"]

    return render(
        request,
        "checkout.html",
        {
            "address": address,
            "cart_data": cart_data,
            "total": total,
        },
    )


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    try:
        user_profile = UserProfile.objects.get(userid=request.user)
    except UserProfile.DoesNotExist:
        return redirect("/addprofile")

    if not Address.objects.filter(userid=request.user).exists():
        return redirect("/addaddress")

    cart_items = Carts.objects.filter(userid=request.user)
    if not cart_items.exists():
        return redirect("/showcarts")

    # Calculate subtotal for each item and total amount
    cart_data = []
    total = 0
    for item in cart_items:
        subtotal = item.qty * item.productid.price
        cart_data.append(
            {
                "productname": item.productid.productname,
                "qty": item.qty,
                "price": item.productid.price,
                "subtotal": subtotal,
            }
        )
        total += subtotal

    return render(
        request,
        "checkout.html",
        {
            "cart_data": cart_data,
            "user_profile": user_profile,
            "address": Address.objects.filter(userid=request.user),
            "total": total,
        },
    )


from .forms import UserProfileForm, AddressForm


def addprofile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.userid = request.user
            profile.save()
            return redirect("/checkout")
    else:
        form = UserProfileForm()
    return render(request, "addprofile.html", {"form": form})


def addaddress(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.userid = request.user
            address.save()
            return redirect("/checkout")
    else:
        form = AddressForm()
    return render(request, "addaddress.html", {"form": form})


def add_to_wishlist(request, productid):
    if request.user.is_authenticated:
        userid = request.user
        product = get_object_or_404(Products, productid=productid)

        # Check if the product is already in the wishlist
        if not Wishlist.objects.filter(userid=userid, productid=product).exists():
            Wishlist.objects.create(userid=userid, productid=product)
            messages.success(request, "Product added to wishlist!")
        else:
            messages.info(request, "Product is already in your wishlist.")

        return redirect("view_wishlist")  # Or redirect to wishlist page
    else:
        messages.error(request, "You need to log in to add products to your wishlist.")
        return redirect("signin")  # Redirect to login page


def remove_from_wishlist(request, productid):
    if request.user.is_authenticated:
        userid = request.user
        product = get_object_or_404(Products, productid=productid)

        wishlist_item = Wishlist.objects.filter(
            userid=userid, productid=product
        ).first()
        if wishlist_item:
            wishlist_item.delete()
            messages.success(request, "Product removed from wishlist.")
        else:
            messages.info(request, "Product is not in your wishlist.")

        return redirect("view_wishlist")  # Or redirect to wishlist page
    else:
        messages.error(
            request, "You need to log in to remove products from your wishlist."
        )
        return redirect("signin")  # Redirect to login page


def view_wishlist(request):
    if request.user.is_authenticated:
        userid = request.user
        wishlist_items = Wishlist.objects.filter(userid=userid)

        context = {
            "wishlist_items": wishlist_items,
        }

        return render(request, "view_wishlist.html", context)
    else:
        messages.error(request, "You need to log in to view your wishlist.")
        return redirect("signin")  # Redirect to login page
