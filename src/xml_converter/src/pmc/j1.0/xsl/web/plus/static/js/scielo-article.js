var sa = {
	Init: function() {
		var p = $("section article .paragraph");
		
		for(var i = 0, l = p.length; i<l; i++) {
			var c = $("p",p[i]).outerHeight(), r = $(".refList",p[i]), rh = r.outerHeight();
			if(rh > c) {
				r.addClass("outer").css("height",c);
			} 
		}

		sa.DefaultBehaviors();
	},
	FloatLimit: $("#content").offset().top,
	FloatMenu: function() {
		var t = $(window).scrollTop(), f = $(".floatMenu");
		if(t > sa.FloatLimit) {
			f.stop(true,false).animate({
				top: "0px"
			},200);
		} else {
			f.stop(true,false).animate({
				top: "-52px"
			},200);
		}

	},
	DefaultBehaviors: function() {
		$("input[name='link-share']").focus(function() {
			$(this).select();
			if (window.clipboardData && clipboardData.setData) {
				clipboardData.setData('text', $(this).text());
			} 
		}).mouseup(function(e) {
			e.preventDefault();
		});

		$("*[data-toggle='tooltip']").on("mouseenter mouseleave",function() {
			if (window.clipboardData && clipboardData.setData)
				$(this).tooltip("toggle");
		});
		
		$("*[data-toggle='modal']").on("click",function() {
			$(this).tooltip("show");
		});
		
		$(".link-group a.author, .link-group a.copyright").click(function() {
			var d = $(this).next("div");
			var a = $(".link-group .infoContainer");
			
			if(a.length > 1) {
				a.each(function() {
					if(this.className != d.attr("class"))
						$(this).hide();
				});
			}

			if(d.is(":visible"))
				d.stop(true,true).fadeOut("fast");
			else 
				d.stop(true,true).fadeIn("fast");
		});
		
		$(".infoContainer .close").click(function() {
			$(this).parent("div").fadeOut("fast");
		});

		$(".rMenu .fold").on("click",function(e) {
			e.preventDefault();
			var d = $(this).next("div"), s = $(this).find("span");
			
			if(d.is(":visible")) {
				d.slideUp("fast");
				s.text("+");
			} else {
				d.slideDown("fast");
				s.text("-");
			}

		});
		$("article p sup").on("mouseenter mouseleave",function(e) {
			var c = this.className;
			c = c.replace("xref ","");
			var b = $("li."+c), p = b.parent("ul");

			if(c.indexOf(" ") >= 0) {
				c = c.split(" ");
				c = "li." + c.join(",li.");
				b = $(c);
				p = b.parent("ul");
			}
			if(e.type === "mouseenter") {
				p.addClass("full");
				b.addClass("highlight").find(".opened").fadeIn("fast");
			} else {
				p.removeClass("full");
				b.removeClass("highlight").find(".opened").hide();
			}
		});
		$("article .span4 .refList li").on("mouseenter mouseleave",function(e) {
			var p = $(this).parent("ul");
			if(e.type === "mouseenter") {
				p.addClass("full");
				$(this).addClass("highlight").find(".opened").fadeIn("fast");
			} else {
				p.removeClass("full");
				$(this).removeClass("highlight").find(".opened").hide();
			}
		});
		$(".iframeModal").click(function(e) {
			e.preventDefault();
			var src = $(this).attr("href"), t = $(this).text(), w = $(window).outerWidth();
			if(w > 980) {
				$('#iframeModal').modal('show');
        		$('#iframeModal iframe').attr('src', src);
        		$('#iframeModal .modal-header span').html(t);
        	} else
        		window.open(src);
		});
		$('#iframeModal button').click(function () {
			$('#iframeModal iframe').removeAttr('src');
		});
		$(".goto").click(function(e) {
			e.preventDefault();
			var src = $(this).attr("href"), t = $(src).offset().top > 0 ? $(src).offset().top - 60 : 0;
			$('html, body').animate({
			    scrollTop: t
			 }, 2000);
		});
		$(".contrib-trigger").click(function(e) {
			e.preventDefault();
			var h = $("header .contrib-group"), t = this;
			if($(t).is(".author-aff")) {
		 		$(".link-group a.author").trigger("click");
		 	} else if($(t).is(".permission")) {
		 		$(".link-group a.copyright").trigger("click");
		 	}
			$('html, body').animate({
			    scrollTop: (h.offset().top-50)
			 }, 2000);
		});
		$(".changeSkin").click(function(e) {
			e.preventDefault();
			var m = $(this).attr("href");
			m = "skin-"+m.replace("#","");

			$("body").attr("class","").addClass(m);
		});
		$(".thumb").on("mouseenter mouseleave click",function(e) {
			var p = $(this).next("div");
			if(e.type == "mouseenter") {
				p.fadeIn("fast");
			} else if(e.type == "mouseleave") {
				p.fadeOut("fast");
			} else if(e.type == "click") {
				window.open(p.find("img").attr("src"));
			}
		});
	}
}

$(document).ready(sa.Init);
$(document).scroll(sa.FloatMenu);