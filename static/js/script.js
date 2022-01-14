$(document).ready(function ($) {
  $(".header__list li").hover(
    function () {
      $(this).find(".header__link").css({ color: "#2855CB" });
      $(this).find(".header__dropdown").stop().slideDown("fast");
    },
    function () {
      if ($(window).width() < 760) {
        $(this).find(".header__link").css({ color: "#212529" });
      } else {
        $(this).find(".header__link").css({ color: "#212529" });
      }
      $(this).find(".header__dropdown").stop().slideUp("fast");
    }
  );
  $(".header__link").mousedown(function (event) {
    $(this).css({ color: "#616161" });
  });
  $(".header__link").mouseup(function (event) {
    $(this).css({ color: "#2855CB" });
  });

  $(".programs__link").click(function (event) {
    var program = $(this).attr("id");
    $(".programs__link").removeClass("active");
    $(this).addClass("active");
    console.log(this, program);
    $(".programs__img").removeClass("visible");
    $(".programs__text").removeClass("visible");
    $(".programs__img[program = " + program + "]").addClass("visible");
    $(".programs__text[program = " + program + "]").addClass("visible");
    if ($(window).width() <= 760) {
      $(".programs__img-wrap").appendTo($(this).parent());
      $(".programs__list").appendTo($(this).parent());
    }
  });

  if ($(window).width() <= 760) {
    $(".header__logo img").attr("src", "./img/mob-logo.png");
    $(".programs__img-wrap").appendTo(
      $(".programs__link[id='economics']").parent()
    );
    $(".programs__list").appendTo(
      $(".programs__link[id='economics']").parent()
    );
    $(".projects__item img").each(function (i) {
      $(this).prependTo($(this).parent());
    });
  }

  setTimeout(typing, 500);

  let burgerOpened = false;
  $(".header__burger-btn").click(function (event) {
    $(".burger__line").toggleClass("active");
    $(".header__list").toggleClass("mobile-active");
    $(".header__list").slideToggle("fast");
  });

  $("img").each(function (i) {
    if ($(this).attr("src") == "") {
      $(this).attr("src", "./img/no-photo.svg");
    }
  });
});
function typing() {
  $(".content__tagline").text("");
  var text = "Раскройте весь потенциал своего ребенка!";
  var count = 0;
  var speed = 75;
  var length = text.length;
  function character(start, end, text) {
    return text.substring(start, end);
  }
  function type() {
    var char = character(count, count + 1, text);
    if (count == 8 || count == 23) {
      $(".content__tagline").append(char);
      $(".content__tagline").append("<br>");
    } else $(".content__tagline").append(char);
    count++;
    if (count < length) setTimeout(type, speed);
    else return;
  }
  type();
}
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}
window.onclick = function(event) {
	  if (!event.target.matches('.dropbtn')) {
		var dropdowns = document.getElementsByClassName("dropdown-content");
		var i;
		for (i = 0; i < dropdowns.length; i++) {
		  var openDropdown = dropdowns[i];
		  if (openDropdown.classList.contains('show')) {
			openDropdown.classList.remove('show');
		  }
		}
	  }
	}
function myFunction_head() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}
var modal3 = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal3) {
        modal3.style.display = "none";
    }
}
