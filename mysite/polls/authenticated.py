from django.shortcuts import redirect, reverse


def is_authenticated(fn):
    def inner(request, *args, **kwargs):
        status = request.session.get('user')
        if status:
            ret = fn(request)
            return ret
        else:
            return redirect(reverse('login'))

    return inner
