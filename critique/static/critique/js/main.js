(function($) {

    function Field($jqElem, validator) {
        this.$elem = $jqElem; 
        this.defaultValue = $jqElem.val();
        this.validator = validator;
    }

    var $wrapper = $('div#dj-critique'),
        $prompt = $('div#dj-critique-prompt', $wrapper),
        $form = $('form#dj-critique-create', $wrapper),
        $submit = $('input#dj-critique-submit', $form),
        $cancel = $('input#dj-critique-cancel', $form),
        $feedback = $('div#dj-critique-feedback', $form),
        config = {
            delay: 3000,
            rate: 200
        },
        fields = {};

    function afterError() {
        setTimeout(function() {
            $feedback.fadeOut();
        }, config.delay); 
    }

    function afterSuccess() {
        setTimeout(function() {
            $feedback.fadeOut(config.rate, function() {
                hideForm(resetMessage);
            });
        }, config.delay); 
    }

    function bindHandlers() {
        fields.email.$elem.on('focus blur', function(e) {
            handleField(e, fields.email);
        });

        fields.message.$elem.on('focus blur', function(e) {
            handleField(e, fields.message);
        });

        // unregister and explicitly handle branching multiple submit inputs
        $form.submit(function() { return false; });

        $cancel.on('click', function() {
            hideForm();
        });

        $submit.on('click', function() {
            // capture current form state
            handleSubmit($('form#dj-critique-create', $wrapper));
        })

        $prompt.on('click', function() {
            $form.slideToggle();
        });
    }

    function configureFields() {
        fields.email = new Field(
            $('input#dj-critique-email', $form),
            djCritique.utils.validateEmail);
        fields.message = new Field(
            $('textarea#dj-critique-message', $form), validateMessage);

        fields.email.$elem.val(djCritique.cookie.get(
            'dj-critique-author', 'Email'));
    }

    function displayFeedback(message, callback) {
        $feedback.find('p').text(message).parent().fadeIn(
                config.rate, function() {
            if (callback) { callback(); }
        });
    }

    function handleField(e, field) {
        var f = field;
        if (e.type == 'focus') {
            if (f.$elem.val() == f.defaultValue) {
                f.$elem.val('');
            }
        } else if (e.type == 'blur') {
            if (!f.$elem.val()) { // user did not type anything
                f.$elem.val(f.defaultValue);
            }
        } else {}
    }

    function handleSubmit($form) {
        var $submits = $submit.add($cancel),
            errors = validateFields();

        toggleHighlightErrors(fields, false);
        $submits.attr('disabled', 'disabled');

        if (errors.length > 0) {
            toggleHighlightErrors(errors, true);
            displayFeedback('Invalid submission!', afterError); 
        } else {
            djCritique.cookie.set('dj-critique-author',
                $('input#dj-critique-email', $form).val())

            $.ajax({
                data: $form.serialize() + '&url=' + window.location.pathname,
                type: 'POST',
                url: '/critique/create/',
                success: function(response) {
                    if (response == 'OK') {
                        toggleHighlightErrors(fields, false);
                        displayFeedback('Success!', afterSuccess); 
                    } else {
                        displayFeedback('Error!', afterError); 
                    }
                }
            });
        }
        $submits.removeAttr('disabled', '');
    }


    function hideForm(callback) {
        $form.slideUp(config.rate, function() {
            if (callback) { callback(); }
        });
    }

    function toggleHighlightErrors(f, flag) {
        for (var i in f) {
            f[i].$elem.toggleClass('dj-critique-error', flag);
        }
    }
    
    function resetMessage() {
        fields.message.$elem.val(fields.message.defaultValue);
    }

    function validateFields() {
        var errors = [], f;

        for (var i in fields) {
            f = fields[i];

            // check for default
            if (f.$elem.val() == f.defaultValue) {
                errors.push(f);
                continue;
            }
            // call validator
            if (!f.validator(f.$elem.val())) {
                errors.push(f);
            }
        }
        return errors;
    }

    function validateMessage(message) {
        if (message.length > 3) {
            return true;
        } else {
            return false;
        }
    }

    // main
    (function() {
        configureFields();
        bindHandlers();
    })();

})(jQuery);
