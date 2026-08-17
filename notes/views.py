from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NoteForm
from .models import Note

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()

            return redirect("note_list")

    else:
        form = NoteForm()

    return render(
        request,
        "notes/note_form.html",
        {
            "form": form,
        },
    )

@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user)

    return render(
        request,
        "notes/note_list.html",
        {
            "notes": notes,
        },
    )

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(
        Note,
        id = note_id,
        owner = request.user,

        #মানে:
    # এই ID-এর Note আছে এবং সেটা current user-এর হলে Note দাও, না হলে 404 দেখাও।
     # এটাই ownership-এর একটা গুরুত্বপূর্ণ security layer।
    )
    return render (request,"notes/note_detail.html",{"note": note})