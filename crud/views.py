import datetime

from django.urls import reverse_lazy
from django.views import generic

from .models import Todo
from crud.forms import TodoForm


class CreateListTodo(generic.CreateView):
    """View for creating and listing todos."""
    template_name = 'crud/todo_list.html'
    form_class = TodoForm
    success_url = reverse_lazy('view:list_view')

    def get_initial(self):
        """The initial values for the create form."""
        now = datetime.datetime.now()
        # Round up minutes to next quarter hour
        init_dt = now + (datetime.datetime.min - now) % datetime.timedelta(minutes=15)
        return {
            'text': 'Whatcha gotta do?',
            'due_at': init_dt
        }

    def get_context_data(self, **kwargs):
        """Get the list of todos for the list view."""
        kwargs['todo_list'] = Todo.objects.order_by('-created_at').all()
        return super(CreateListTodo, self).get_context_data(**kwargs)


class UpdateTodo(generic.UpdateView):
    """Update an existing Todo entry using the create form."""
    template_name = 'crud/todo_form.html'
    form_class = TodoForm
    success_url = reverse_lazy('view:list_view')

    def get_queryset(self):
        """Fetch the correct item via primary key."""
        query_set = Todo.objects.filter(pk=self.kwargs['pk'])
        return query_set


class DeleteTodo(generic.DeleteView):
    """Delete an existing Todo entry."""
    model = Todo
    success_url = reverse_lazy('view:list_view')
