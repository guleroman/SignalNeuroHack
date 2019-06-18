
var form = $('.form');
var btn = $('#submit');
var topbar = $('.topbar');
var input = $('#password');
var article =$('.article');
var tries = 0;
var h = input.height();
$('.spanColor').height(h+23);
$('#findpass').on('click',function(){
  $(this).text('1234');
});
input.on('focus',function(){
  topbar.removeClass('error success');
  input.text('');
});
btn.on('click',function(){
  if(tries<=2){
    var pass = $('#password').val();
    console.log(pass);
    if(pass==='1234'){
    setTimeout(function(){
      btn.text('Success!');
    },250);
    topbar.addClass('success');
    form.addClass('goAway');
    article.addClass('active');
    tries=0;
  }
    else{
      topbar.addClass('error');
      tries++;
      switch(tries){
        case 0:
          btn.text('Login');
          break;
        case 1:
          setTimeout(function(){
          btn.text('You have 2 tries left');
          },300);
          break;
        case 2:
          setTimeout(function(){
          btn.text('Only 1 more');
          },300);
          break;
        case 3:
          setTimeout(function(){
          btn.text('Recover password?');
          },300);
          input.prop('disabled',true);
          topbar.removeClass('error');
          input.addClass('disabled');
          btn.addClass('recover');
          break;
         defaut:
          btn.text('Login');
          break;
      }
    } 
  }
  else{
    topbar.addClass('disabled');
  }
  
});

$('.form').keypress(function(e){
   if(e.keyCode==13)
   submit.click();
});
input.keypress(function(){
  topbar.removeClass('success error');
});



$(function () {
  var totalTime = 6, // seconds
      percent = 0,
      $sIcon = $('.success-icon'),
      $sText = $('.success-text'),
      $info = $('.timer-info'),
      $bar = $('.timer-bar'),
      $dropZone = $('.drop-zone'),
      dropZone = $('.drop-zone')[0],
      width = $dropZone.width(),
      countdown,
      countdownOver = false;

  var startCountdown = function () {
      $dropZone.css('border', 'none');
      $dropZone.addClass('timer-bar-wrapper');
      $info.text('0%');
      countdown = setInterval(updateBar, 25);
  };

  $(window).resize(function () {
      if (countdownOver) {
          width = $dropZone.width();
          $dropZone.css('height', width);
      }
  });

  var fileStatus = function () {
      $sIcon
          .addClass('up')
          .delay(250)
          .fadeTo(250, 1, 'swing');
      $sText
          .text('File uploaded')
          .delay(500)
          .fadeTo(350, 1, 'swing');
      $dropZone.css('transition', 'none');
  };

  var triggerFinish = function () {
      $dropZone
          .css('height', width)
          .addClass('expand');
      $info.fadeTo(250, 0, 'swing');
      setTimeout(fileStatus, 700);
  };

  var stopCountdown = function () {
      clearInterval(countdown);
      $('.timer-info').text('100%');
      triggerFinish();
  };

  var updateBar = function () {
      percent++;
      // /40, because it's called every 25ms
      // -> 25ms * 40 = 1 sec
      var per = (100 * percent / totalTime) / 40;
      $bar.css('width', per + '%');
      $info
          .css('left', per + '%')
          .text(per.toFixed(1) + '%');
      if (per >= 100) {
          stopCountdown();
          countdownOver = true;
      }
  };

  dropZone.addEventListener('dragover', function (e) {
      e.stopPropagation();
      e.preventDefault();
  });
  dropZone.addEventListener('drop', function (e) {
      e.stopPropagation();
      e.preventDefault();
      
      setTimeout(startCountdown, 250)
  });
});
