// (C) 2015 by Yefei

var Web = {};

$.ajaxSetup({cache:false, dataType:'json'});

$.ajaxPrefilter(function(options, originalOptions, xhr){
	if (!options.crossDomain) {
		var token = $('meta[name="csrf-token"]').attr('content');
		if (token) xhr.setRequestHeader('X-CSRFToken', token);
	}
});

if (window.HTMLAudioElement) {
	Web._notify_audio = new Audio();
	Web._notify_audio.src = static_prefix + 'audio/notify.wav';
}

Web.notify = function(tags, message){
	$().toastmessage('showToast', {text:message, type:tags});
	if (Web._notify_audio) Web._notify_audio.play();
};

Web.modal_defaults = {
	header: null,
	body: '',
	footer: null,
	closeButton: '<button class="btn" data-dismiss="modal" aria-hidden="true">关闭</button>',
	// bootstrap model options
	backdrop: true,
	keyboard: true,
	show: true,
	remote: false
	
};
Web.modal = function(options){
	var opts = $.extend({}, Web.modal_defaults, options);
	var header = null, footer = null;
	
	if (opts.header) {
		header = $('<div></div>').addClass('modal-header').append(opts.header);
	}
	
	if (opts.footer || opts.closeButton) {
		footer = $('<div></div>').addClass('modal-footer');
		opts.footer && footer.append(opts.footer);
		opts.closeButton && footer.append(opts.closeButton);
	}
	
	var body = $('<div></div>').addClass('modal-body').append(opts.body);
	var modal = $('<div></div>').addClass('modal fade').append(header).append(body).append(footer).modal({
		backdrop: opts.backdrop,
		keyboard: opts.keyboard,
		show: opts.show,
		remote: opts.remote
	});
	
	modal.on('hidden', function(){
		$(this).remove();
	});
};

$(document).ajaxError(function(event, xhr, ajaxSettings, thrownError){
	if (xhr.status >= 500 && xhr.status < 600) {
		Web.notify('error', '500: 服务器程序错误');
	}
	else if (xhr.status == 401) {
		Web.notify('error', '401: 未授权，请登陆帐号');
	}
	else if (xhr.status == 403) {
		Web.notify('error', '403: 没有权限');
	}
	else if (xhr.status == 404) {
		Web.notify('error', '404: 请求的资源不存在');
	}
	else if (xhr.status == 422) {
		var data = $.parseJSON(xhr.responseText);
		switch (data.type) {
		case 'FormError':
			var body = $('<div class="form-error"></div>');
			body.html($.map(data.message, function(v){
				return '<p>' + (v.label?'<label>'+v.label+'：</label>':'') + v.message + '</p>';
			}));
			Web.modal({body:body, header:'<b>请修正以下问题</b>'});
			break;
		case 'Deny':
			Web.modal({body:data.message, header:'<b>操作被禁止</b>'});
			break;
		}
	}
});
