window.taskcardmaker = window.taskcardmaker || {};
window.ui = window.ui || {};

ui.Dialog = function (selector, title) {
	var dialog = jQuery(selector).dialog({
		autoOpen: false,
		modal: true,
		title: title
	});
	
	this.toggle = function () {
		if (dialog.dialog('isOpen')) {
			dialog.dialog('close');
		} else {
			dialog.dialog('open');
		}
	};
};

ui.Checkbox = function (label, name, id, checked, callback) {
	var group = jQuery("<div>");
	var input = jQuery("<input type='checkbox'>").appendTo(group).attr("name",
			name).attr("id", id);
	
	if (checked) {
		console.log("Checking " + name);
		input.attr("checked", true);
	} else {
		console.log("Unchecking " + name);
		input.attr("checked", false);
	}

	input.change(function() {
		callback(input.attr("checked"));
	});

	jQuery("<label>").attr("for", name).text(label).appendTo(group);

	return group;
};

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
	
	function parseBoolean (string) {
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
		if (autoUpdatePreview == null) {
			autoUpdatePreview = "true";
		}
		this.autoupdatePreview = parseBoolean(autoUpdatePreview);
	};

	this.load();
	console.log(this.autoupdatePreview);

	var dialog = new ui.Dialog(containerExpr, 'Preferences');
	var container = jQuery(containerExpr);
	container.hide();

	var fieldset = jQuery("<fieldset>").appendTo(container);
	jQuery("<legend>").text("Preferences").appendTo(fieldset);

	new ui.Checkbox("Update the preview everytime I press return",
			"autoupdate", "input-autoupdate", this.autoupdatePreview, function(
					checked) {
				that.autoupdatePreview = checked;
				that.save();
			}).appendTo(fieldset);

	/*
	new ui.Checkbox("Generate story card for each story", "generateStoryCards",
			"input-generate-story-cards", this.generateStoryCards, function(
					checked) {
				that.generateStoryCards = checked;
				that.save();
			}).appendTo(fieldset);

	new ui.Checkbox("Add background colors for cards", "colorCards",
			"input-color-cards", this.colorCards, function(checked) {
				that.colorCards = checked;
				that.save();
			}).appendTo(fieldset);
	*/

	this.toggle = function() {
		dialog.toggle();
	};
};

taskcardmaker.Editor = function() {
	this.downloadPdf = function() {
		jQuery("#pdf-form").submit();
	};

	this.showError = function(text) {
		jQuery("#preview").html('<span class="error">' + text + '</span>');
	};

	function showPreviewObject(project) {
		jQuery("#preview").html("");

		for ( var i = 0; i < project.stories.length; ++i) {
			var story = project.stories[i];

			var storyCard = jQuery("<div>");
			storyCard.appendTo("#preview");
			storyCard.addClass("card").addClass("story");
			jQuery("<div>").appendTo(storyCard).addClass("identifier").text(
					story.identifier);
			jQuery("<div>").appendTo(storyCard).addClass("title").text(
					story.title);

			for ( var j = 0; j < story.tasks.length; ++j) {
				var task = story.tasks[j];

				var taskCard = jQuery("<div>");
				taskCard.appendTo("#preview");
				taskCard.addClass("card").addClass("task");

				jQuery("<div>").appendTo(taskCard).addClass("story-identifier")
						.text(story.identifier);
				jQuery("<div>").appendTo(taskCard).addClass("description")
						.text(task.description);

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
						showError(data.message);
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
