from django.shortcuts import render
from django import forms
import markdown2
from random import randint

from . import util

term = ""
start_text_new_page = "# Title goes here \n\n Enter text here \n\n link another page like this:\n[HTML](/wiki/HTML)"

class SearchForm(forms.Form):
    term = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': 'distance'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': "Enter title here", 'class': 'distance'}))
    contents = forms.CharField(label="", initial=start_text_new_page, widget=forms.Textarea(attrs={'class': 'distance'}))

class EditPageForm(forms.Form):
    contents = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'distance'}))

def index(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["contents"]
            if title.lower() in [each_title.lower() for each_title in util.list_entries()]:
                return render(request, "encyclopedia/new_page_invalid.html", {
                    "form": SearchForm(), "new_page_form": NewPageForm(request.POST)
                })
            else:
                util.save_entry(title, content)
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": SearchForm()
    })

def entry(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["contents"]
            util.save_entry(title, content)
        else:
            print("Form not valid")
    
    if title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "md_text": markdown2.markdown(util.get_entry(title)), "title": title, "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title, "form": SearchForm()
        })

def random(request):
    title = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/entry.html", {
        "md_text": markdown2.markdown(util.get_entry(title)), "title": title, "form": SearchForm()
    })

def search_results(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data["term"]
        else:
            return render(request, "{% url: 'index' %}", {
                "form": form
            })
    
    results = {}
    count = 0
    for entry in util.list_entries():
        if str(term).lower() == entry.lower():
            return render(request, "encyclopedia/entry.html", {
                "md_text": markdown2.markdown(util.get_entry(entry)), "title": entry, "form": SearchForm()
            })
        elif str(term).lower() in entry.lower():
            results[entry] = first20(markdown2.markdown(util.get_entry(entry)))
            count += 1

    return render(request, "encyclopedia/search_result.html", {
        "form": SearchForm(), "term": term, "results": results
    })

def error(request):
    return render(request, "encyclopedia/error.html", {
        "form": SearchForm()
    })

def new_page(request):    
    return render(request, "encyclopedia/new_page.html", {
        "form": SearchForm(), "new_page_form": NewPageForm()
    })

def edit_page(request, title):
    form = EditPageForm(initial={"contents":util.get_entry(title)})
    return render(request, "encyclopedia/edit.html", {
        "form": SearchForm(), "edit_page_form": form, "title":title
    })

def first20(html_text):
    text = html_text.split("<p>")[1].split("</p>")[0]
    text = text.split()
    if len(text) > 20:
        text = text[:20]
        text.append("...")
    text = ' '.join(text)
    return text

