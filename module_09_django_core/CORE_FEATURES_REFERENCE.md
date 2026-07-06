# Django Core Features Reference

A map of the "batteries included" features and when to reach for each.

## Request / Response Helpers
| Feature | Module | Use it for |
|---|---|---|
| Formsets | django.forms.formset_factory | many copies of one form |
| Pagination | django.core.paginator.Paginator | splitting long lists |
| Sessions | django.contrib.sessions | per-visitor server state |
| Messages | django.contrib.messages | one-time flash notifications |

## Content & SEO
| Feature | Module |
|---|---|
| Syndication feeds | django.contrib.syndication |
| Sitemaps | django.contrib.sitemaps |
| Sites framework | django.contrib.sites |

## Validation & Templates
- Validators: reusable callables run by forms and Model.full_clean().
- Custom template tags/filters live in <app>/templatetags/.

## Internationalization
- Mark strings with gettext / gettext_lazy.
- makemessages -l <lang>  ->  edit .po  ->  compilemessages.
- USE_I18N plus LocaleMiddleware enable runtime language switching.

## Exercises
1. Add a paginated article list with 10 items per page.
2. Show a success message after a form submission and render it.
3. Expose an RSS feed of the 10 newest articles.
4. Translate the navigation bar into a second language.
5. Build a {% custom %} tag that formats prices as currency.