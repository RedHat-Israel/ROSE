How to update/add exercises to course slides
============================================

1. Create an `.md` exercise file. Please follow the styling conventions.  

2. Add a new section in the corresponding `.html` using the following:  
```html
<section data-markdown="relative/path/class_exercise_number.md" data-separator="^\n\n\n" data-separator-vertical="^\n\n">
</section>
```
   - Example path: `"exercises/01_Linux/class_exercise_2.md"`
   - Make sure not to use the abriviation 'exe', the styling of the slides won't work propperly.  

3. To test the slides follow the next steps:
   1. Run `pipenv shell`
   2. Run `python -m http.server 9000` (use a port number of your choosing)
   3. Open your browser on `localhost:9000` and navigate to the wanted slides.