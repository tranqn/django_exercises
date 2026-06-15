# Django Forms Cheatsheet

## Form Field Types
| Field | Widget | HTML |
|---|---|---|
| CharField | TextInput | `<input type="text">` |
| EmailField | EmailInput | `<input type="email">` |
| IntegerField | NumberInput | `<input type="number">` |
| FloatField | NumberInput | `<input type="number">` |
| BooleanField | CheckboxInput | `<input type="checkbox">` |
| DateField | DateInput | `<input type="text">` |
| FileField | FileInput | `<input type="file">` |
| ImageField | FileInput | `<input type="file">` |
| ChoiceField | Select | `<select>` |
| TypedChoiceField | Select | `<select>` (with coercion) |
| MultipleChoiceField | SelectMultiple | `<select multiple>` |
| URLField | URLInput | `<input type="url">` |

## Rendering Options
- `{{ form.as_p }}` — each field in `<p>` tags
- `{{ form.as_table }}` — each field in `<tr>` tags
- `{{ form.as_ul }}` — each field in `<li>` tags
- `{{ form.as_div }}` — each field in `<div>` tags (Django 5+)
- Manual: `{{ field.label_tag }}` `{{ field }}` `{{ field.errors }}`

## Validation Order
1. `field.clean()` — built-in field validation
2. `clean_<fieldname>()` — custom field-level validation
3. `clean()` — cross-field validation