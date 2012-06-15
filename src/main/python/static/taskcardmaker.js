window.taskcardmaker = window.taskcardmaker || {};
window.ui = window.ui || {};

taskcardmaker.Preferences = function(containerExpr) {
	var that = this;

	this.autoupdatePreview = true;
	this.generateStoryCards = true;
	this.colorCards = true;

	function booleanString(value) {
		if (value) {
			return "true";
		}
		return "false";
	}

	function parseBoolean(string) {
		if (!string) {
			return false;
		}
		return string.toLowerCase() === "true";
	}

	this.save = function() {
		if (!window.localStorage) {
			return;
		}

		localStorage.setItem("autoUpdatePreview",
				booleanString(this.autoupdatePreview));
	};

	this.load = function() {
		if (!window.localStorage) {
			return;
		}
		var autoUpdatePreview = localStorage.getItem("autoUpdatePreview");
		if (autoUpdatePreview === null) {
			autoUpdatePreview = "true";
		}
		this.autoupdatePreview = parseBoolean(autoUpdatePreview);
	};

	this.load();
	
	var position = [jQuery(window).width() - 430, 
	                30];
	
	var dialog = jQuery(containerExpr).dialog({
		autoOpen : false,
		modal : false,
		resizable: false,
		position: position, 
		title : "Preferences",
		draggable: false,
		width: 400,
		dialogClass: "preferences-dialog"
	});

	dialog.toggle = function() {
		if (dialog.dialog('isOpen')) {
			dialog.dialog('close');
		} else {
			dialog.dialog('open');
		}
	};

	dialog.hide();

	jQuery("#input-autoupdate").attr("checked", this.autoUpdatePreview ? "checked" : "");
	jQuery("#input-autoupdate").change(function() {
		console.log("Changing autoupdate");
		var checked = jQuery(this).attr("checked");
		that.autoupdatePreview = checked;
		that.save();
	});

	jQuery("#input-generate-story-cards").change(function() {
		var checked = jQuery(this).attr("checked");
		that.generateStoryCards = checked;
		that.save();
	});

	jQuery("#input-color-cards").change(function() {
		var checked = jQuery(this).attr("checked");
		that.colorCards = checked;
		that.save();
	});

	this.toggle = function() {
		dialog.toggle();
	};
};

taskcardmaker.Editor = function() {
	var that = this;
	
	this.downloadPdf = function() {
		jQuery("#pdf-form").submit();
	};
	
	this.sendEmail = function () {
		var sourceCode = jQuery("#editor").val();

		jQuery.ajax({
			type : "POST",
			url : "/email",
			data : sourceCode,
			dataType : "json",
			success : function(data) {
				if (data.status === 200) {
					that.showMessage("Email has been sent.");
				} else {
					that.showError(data.message);
				}
			}
		});
	};

	this.showError = function(text) {
		jQuery("#preview").html('<span class="error">' + text + '</span>');
	};
	
	function buildMultilineString (listOfStrings) {
		var result = "";

		for (var k = 0; k < listOfStrings.length; ++k) {
			result += listOfStrings[k] + "<br/>";
		}
		
		return result;
	}
	

	function showPreviewObject(project) {
		jQuery("#preview").html("");

		for ( var i = 0; i < project.stories.length; ++i) {
			var story = project.stories[i];

			var storyCard = jQuery("<div>");
			storyCard.appendTo("#preview");
			storyCard.addClass("card").addClass("story");
			jQuery("<div>").appendTo(storyCard).addClass("identifier").text(
					story.identifier);
			jQuery("<div>").appendTo(storyCard).addClass("title").html(
					buildMultilineString(story.title));

			for ( var j = 0; j < story.tasks.length; ++j) {
				var task = story.tasks[j];

				var taskCard = jQuery("<div>");
				taskCard.appendTo("#preview");
				taskCard.addClass("card").addClass("task");

				jQuery("<div>").appendTo(taskCard).addClass("story-identifier")
						.text(story.identifier);

				jQuery("<div>")
					.appendTo(taskCard)
					.addClass("description")
					.html(buildMultilineString(task.description));

				var tagsText = "";
				for ( var t = 0; t < task.tags.length; ++t) {
					tagsText += task.tags[t] + " ";
				}

				jQuery("<div>").appendTo(taskCard).addClass("tags").text(
						tagsText);

				if (task.blocker) {
					taskCard.addClass("blocker");
				}
			}
		}
	}
	this.showPreview = function(withAnimation) {
		var sourceCode = jQuery("#editor").val();

		if (withAnimation) {
			jQuery("#preview").fadeOut(150, function() {
				jQuery("#wait-indicator").fadeIn(150);
			});
		} else {
			jQuery('#preview').hide();
			jQuery('#wait-indicator').show();
		}

		window.setTimeout(function() {
			jQuery.ajax({
				type : "POST",
				url : "/parse",
				data : sourceCode,
				dataType : "json",
				success : function(data) {
					if (data.status === 200) {
						showPreviewObject(data.project);
					} else {
						that.showError(data.message);
					}

					if (withAnimation) {
						jQuery("#wait-indicator").fadeOut(150, function() {
							jQuery("#preview").fadeIn(150);
						});
					} else {
						jQuery('#wait-indicator').hide();
						jQuery('#preview').show();
					}
				}
			})
		}, withAnimation ? 200 : 1);
	}

	this.showMessage = function(message) {
		var div = jQuery("<div>").appendTo(jQuery(document.body));
		div.hide();
		div.attr("id", "message");

		jQuery("<span>").appendTo(div).html(message);
		jQuery("<a>").appendTo(div).css("padding-left", "1em")
				.attr("href", "#").text("hide").click(function() {
					div.fadeOut();
				});

		var width = $(window).width();
		var divWidth = div.width();
		div.css("left", ((width - divWidth) / 2) + "px");

		div.fadeIn();
	};
};

taskcardmaker.utils = taskcardmaker.utils || {};
taskcardmaker.utils.isBrowserOutdated = function() {
	return !window.localStorage
			|| ((!jQuery.browser.webkit) && (!jQuery.browser.mozilla));
};
