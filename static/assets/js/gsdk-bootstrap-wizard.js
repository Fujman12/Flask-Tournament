/*!

 =========================================================
 * Bootstrap Wizard - v1.1.1
 =========================================================

 * Product Page: https://www.creative-tim.com/product/bootstrap-wizard
 * Copyright 2017 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/bootstrap-wizard/blob/master/LICENSE.md)

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 */

// Get Shit Done Kit Bootstrap Wizard Functions

setTimeout(() => {
  document.querySelector('#select-participant').click()
  setTimeout(() => document.querySelector('.btn.btn-primary.btn-block.participant-select-button').click(), 500)
}, 1000)

(function() {
  var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
    window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
  window.requestAnimationFrame = requestAnimationFrame;
})();

searchVisible = 0;
transparent = true;

function some(round_number){

  /*  Activate the tooltips      */
  $('[rel="tooltip"]').tooltip();

  // Code for the Validator
  var $validator = $('.wizard-card form').validate({
    rules: {
      firstname: {
        required: true,
        minlength: 3
      },
      lastname: {
        required: true,
        minlength: 3
      },
      email: {
        required: true,
        minlength: 3,
      }
    }
  });

  // round_number = 2;

  globalConfig.round_number = round_number;

  generateTabs(round_number < 3 ? round_number : 3)
  generateQuestions(round_number < 3 ? round_number : 3, +round_number === 1 ? round_number : 2)

  // Wizard Initialization
  $('.wizard-card').bootstrapWizard({
    'tabClass': 'nav nav-pills',
    'nextSelector': '.btn-next',
    'previousSelector': '.btn-previous',

    onNext: function(tab, navigation, index) {
      var $valid = $('.wizard-card form').valid();
      if(!$valid) {
        $validator.focusInvalid();
        return false;
      }
    },

    onInit : function(tab, navigation, index){

      //check number of tabs and fill the entire row
      var $total = navigation.find('li').length;
      $width = 100/$total;
      var $wizard = navigation.closest('.wizard-card');

      $display_width = $(document).width();

      if($display_width < 600 && $total > 3){
        $width = 50;
      }

      navigation.find('li').css('width',$width + '%');
      $first_li = navigation.find('li:first-child a').html();
      $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
      $('.wizard-card .wizard-navigation').append($moving_div);
      refreshAnimation($wizard, index);
      $('.moving-tab').css('transition','transform 0s');
    },

    onTabClick : function(tab, navigation, index){

      var $valid = $('.wizard-card form').valid();

      if(!$valid){
        return false;
      } else {
        return true;
      }
    },

    onTabShow: function(tab, navigation, index) {
      var $total = navigation.find('li').length;
      var $current = index+1;

      var $wizard = navigation.closest('.wizard-card');

      // If it's the last tab then hide the last button and show the finish instead
      if($current >= $total) {
        $($wizard).find('.btn-next').hide();
        $($wizard).find('.btn-finish').show();
      } else {
        $($wizard).find('.btn-next').show();
        $($wizard).find('.btn-finish').hide();
      }

      button_text = navigation.find('li:nth-child(' + $current + ') a').html();

      setTimeout(function(){
        $('.moving-tab').text(button_text);
      }, 150);

      var checkbox = $('.footer-checkbox');

      if( !index == 0 ){
        $(checkbox).css({
          'opacity':'0',
          'visibility':'hidden',
          'position':'absolute'
        });
      } else {
        $(checkbox).css({
          'opacity':'1',
          'visibility':'visible'
        });
      }

      refreshAnimation($wizard, index);
    }
  });

  // Prepare the preview for profile picture
  $("#wizard-picture").change(function(){
    readURL(this);
  });

  $('[data-toggle="wizard-radio"]').click(function(){
    wizard = $(this).closest('.wizard-card');
    wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
    $(this).addClass('active');
    $(wizard).find('[type="radio"]').removeAttr('checked');
    $(this).find('[type="radio"]').attr('checked','true');
  });

  $('[data-toggle="wizard-checkbox"]').click(function(){
    if( $(this).hasClass('active')){
      $(this).removeClass('active');
      $(this).find('[type="checkbox"]').removeAttr('checked');
    } else {
      $(this).addClass('active');
      $(this).find('[type="checkbox"]').attr('checked','true');
    }
  });

  $('.set-full-height').css('height', 'auto');

};



//Function to show image before upload

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
    }
    reader.readAsDataURL(input.files[0]);
  }
}

$(window).resize(function(){
  $('.wizard-card').each(function(){
    $wizard = $(this);
    index = $wizard.bootstrapWizard('currentIndex');
    refreshAnimation($wizard, index);

    $('.moving-tab').css({
      'transition': 'transform 0s'
    });
  });
});

function refreshAnimation($wizard, index){
  var round_number = globalConfig.round_number < 3 ? globalConfig.round_number : 3
  total_steps = globalConfig.tabs[round_number - 1].content.length;
  move_distance = $wizard.width() / total_steps * index;

  $wizard.find('.moving-tab').css('width', 100 / total_steps + '%');
  $('.moving-tab').css({
    'transform':'translate3d(' + move_distance + 'px, 0, 0)',
    'transition': 'all 0.3s ease-out'
  });
}

function generateTabs(index) {
  var content = ''
  var tabs = globalConfig.tabs[index - 1].content

  for (var i = 0; i < tabs.length; i++) {
    content += '<li style="width: ' + 100 / tabs.length + '%;">' +
      '<a href="#round-' + index + '-' + (i + 1) + '" data-toggle="tab" class="" aria-expanded="false">' +
        tabs[i].label.title +
      '</a>' +
    '</li>'
  }

  $('.wizard-navigation .nav-pills').html(content)
}

function generateRates(question, index, teamId) {
  var scores = '<div class="wizard-content-line-first-part__score">' +
    '<ul>'

  var scoreRange = question.scoreRange
    ? question.scoreRange
    : globalConfig.tabs[index - 1].scoreRange

  for (let scoreN = scoreRange[0]; scoreN <= scoreRange[1]; scoreN++) {
    scores += '<li style="margin-right: 5px;" data-index="' +
      question.index +
    '" data-team-id="' +
      teamId +
    '" data-value="' +
      scoreN +
    '"' +
    '>' +
      '<a>' +
        scoreN +
      '</a>' +
    '</li>'
  }

  scores += '</ul></div>'

  return scores
}

function generateQuestions(index, teams) {
  var content = ''
  var tabQuestions = globalConfig.tabs[index - 1].content

  for (var idx = 0; idx < tabQuestions.length; idx++) {
    content = ''
    var questions = tabQuestions[idx].questions

    if (tabQuestions[idx].label.subtitle) {
      $('#round-' + index + '-' + (idx + 1) + '-second-title').text(tabQuestions[idx].label.subtitle)
    }

    for (var i = 0; i < questions.length; i++) {
      var question = questions[i]
      var tag = question.isSubTitle ? 3 : 4
      var scores = ''

      if (!question.isSubTitle) {
        scores = generateRates(question, index, 1)
        scores += +teams === 2 ? generateRates(question, index, 2) : ''
      }

      content += '<div class="wizard-content-wrapper__question">' +
        '<h' + tag + ' style="margin-bottom: 28px; max-width: 65%">' +
          question.text +
        '</h' + tag + '>' +
        '<div style="display: flex;">' +
          scores +
        '</div>' +
      '</div>'
    }
    $('#round-' + index + '-' + (idx + 1) + ' > div > div:nth-of-type(1)').html(content)

    $('#round-' + index + '-' + (idx + 1) + ' > div > div:nth-of-type(1) li').on('click', function () {
      var el = $(this)
      requestAnimationFrame(function () {
        selectScore(el)
      })
    })
  }
}

function selectScore(el) {
  var parent = el.parent()
  const [
    roundId,
    tabId,
    questId,
  ] = el.data('index').split('-')

  let tab = roundScores
    .find(round => +round.roundId === +roundId).teams
    .find(team => +team.id === +el.data('team-id')).scores
    .find(tab => `${tab.tabId}` === `${roundId}-${tabId}`)

  let questionMark = tab.ratings.find(question => +question.id === +questId)
  let score = el.data('value')

  if (questionMark) {
    questionMark.score = score
  }

  if (!questionMark) {
    tab.ratings.push({
      id: questId,
      score,
    })
  }

  parent.find('li').removeClass('wizard-content-wrapper__li--active')
  parent.find(`li[data-value="${score}"]`).addClass('wizard-content-wrapper__li--active')
}

function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    }, wait);
    if (immediate && !timeout) func.apply(context, args);
  };
};
