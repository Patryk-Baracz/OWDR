document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    if (this.currentStep === 4) {
                        if (fourthStepValidation()) {
                            summary();
                            this.currentStep++;
                            this.updateForm();
                        }
                    }
                    if (this.currentStep === 3) {
                        if (thirdStepValidation()) {
                            this.currentStep++;
                            this.updateForm();
                        }
                    }
                    if (this.currentStep === 2) {
                        if (secondStepValidation()) {
                            this.currentStep++;
                            filterOrganisation();
                            this.updateForm();
                        }
                    }
                    if (this.currentStep === 1) {
                        if (firstStepValidation()) {
                            this.currentStep++;
                            this.updateForm();
                        }
                    }
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    if (this.currentStep === 3) {
                        resetOrganisationFilter();
                    }
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            if (this.currentStep !== 5) {
                e.preventDefault();
                this.currentStep++;
                this.updateForm();
            }
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});

function firstStepValidation() {
    var checkboxElements = document.querySelectorAll(".checkbox-input");
    for (var i = 0; i < checkboxElements.length; i++)
        if (checkboxElements[i].checked)
            return true;
    alert("Zaznacz kategorie!");
    return false;
}

function secondStepValidation() {
    var bagsElement = document.querySelector("#bags");
    if (bagsElement.value >= 1) {
        return true;
    } else {
        alert("Podaj liczbę worków!");
        return false;
    }
}

function thirdStepValidation() {
    var radioElements = document.querySelectorAll(".radio-input");
    for (var i = 0; i < radioElements.length; i++)
        if (radioElements[i].checked)
            return true;
    alert("Zaznacz organizację!");
    return false;
}

function fourthStepValidation() {
    var fourthLabelElements = document.querySelectorAll(".fourth-label");
    var isValid = true
    for (var i = 0; i < fourthLabelElements.length; i++)
        if (fourthLabelElements[i].value === '') {

            isValid = false;
        }
    if (isValid === true) {
        return true;
    } else {
        alert("Uzupełnij dane!");
        return false;
    }
}

function filterOrganisation() {
    var categoriesList = []
    var checkboxElements = document.querySelectorAll(".checkbox-input");
    for (var i = 0; i < checkboxElements.length; i++) {
        if (checkboxElements[i].checked) {
            categoriesList.push(checkboxElements[i].value);
        }
    }
    var organistionsDivs = document.querySelectorAll('.organisations');
    for (var i = 0; i < organistionsDivs.length; i++) {
        var categoriesId = organistionsDivs[i].dataset.categories;
        for (var e = 0; e < categoriesList.length; e++) {
            if (categoriesId.includes(categoriesList[e])) {
            } else {
                organistionsDivs[i].style.visibility = "hidden";
            }
        }
    }
}

function resetOrganisationFilter() {
    var organistionsDivs = document.querySelectorAll('.organisations');
    for (var i = 0; i < organistionsDivs.length; i++) {
        organistionsDivs[i].style.visibility = "visible";
    }
}

function summary() {
    var fourthLabelElements = document.querySelectorAll(".fourth-label");
    var addressSummary = document.querySelectorAll('.address');
    for (var i = 0; i < fourthLabelElements.length; i++) {
        addressSummary[i].innerText = fourthLabelElements[i].value;
    }
    let comments = document.querySelector('#comments');
    let commentsForm = document.querySelector('#comments-form')
    comments.innerText = commentsForm.value;
    let bagsSummary = document.querySelector('#bags-summary')
    let bags = document.querySelector('#bags');
    bagsSummary.innerHTML = bags.value + " * worek darów."
    let organisationSummary = document.querySelector('#organisation-summary');
    var checkboxOrganisation = document.querySelectorAll(".radio-input");
    for (var i = 0; i < checkboxOrganisation.length; i++) {
        if (checkboxOrganisation[i].checked) {
            var organisation = checkboxOrganisation[i].parentElement.lastElementChild.firstElementChild.innerText;
        }
    }
    organisationSummary.innerHTML = "Na rzecz - " + organisation + "."
}