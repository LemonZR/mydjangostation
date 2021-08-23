from django.shortcuts import redirect, reverse


def is_authenticated(fn):
    def inner(request, *args, **kwargs):

        status = request.session.get('user')
        if status:
            ret = fn(request)
            return ret
        else:
            request.session.setdefault('HTTP_REFERER', request.get_full_path())
            return redirect(reverse('login'))

    return inner
