Messenger.options = {
	    extraClasses: 'messenger-fixed messenger-on-bottom messenger-on-right',
	    theme: 'flat'
};

function toast(notification, success){
	Messenger().post({
		message: notification,
		type: success ? "success" : "failure",
		showCloseButton: true,
		hideAfter: 2});
}

angular.module('mypseudoApp.controllers', ["ngResource"]).
controller('ListCtrl', function ListCtrl($scope, $resource, $q){
	var Callbacks = $resource('/callbacks',{},{});

	$scope.callbacks = Callbacks.query(function(){
		for (callback in $scope.callbacks){
			var tmp = $scope.callbacks[callback].last_time;
			if (tmp)
				$scope.callbacks[callback].last_time = prettyDate(new Date(tmp[0],tmp[1] - 1,tmp[2],tmp[3],tmp[4],tmp[5]));
			else
				$scope.callbacks[callback].last_time = 'n/a';
		}
	});

}).
controller('EditCtrl', function EditCtrl($scope, $routeParams, $resource, $http, $q){
	var local_parser_id_counter = 0;
	var local_request_id_counter = 0;
	var tmpCallbackId = $routeParams.callback_id;
	var Callback = $resource('/callback/:id',{id: 'none'});

	$scope.initialized = false;

	$scope.save = function(){
		if ($scope.initialized == true)
			$scope.callback.$save(null, function(){
				toast("Callback successfully saved.", true);
			}, function(){
				toast("Error: Callback could not be saved", false);
			});
		console.log($scope.callback);
	}

	$scope.newParserVar = function(){
		console.log($scope.initialized);
		if ($scope.initialized == true){
			console.log('new parser var');
			$scope.callback.parser_vars.push({local_id: local_parser_id_counter++});
		}
	}

	$scope.newRequestVar = function(){
		console.log($scope.initialized);
		if ($scope.initialized == true){
			console.log('new request var');
			$scope.callback.request_vars.push({local_id: local_request_id_counter++});
		}
	}

	$scope.deleteParserVar = function(local_id){
		console.log($scope.initialized);
		if ($scope.initialized == true){
			var cb = $scope.callback;
			console.log('delete parser var');

			x = new Array();
			for (parser_var in cb.parser_vars)
				if (!(cb.parser_vars[parser_var]['local_id'] == local_id))
					x.push(cb.parser_vars[parser_var]);
				else
					if (cb.parser_vars[parser_var]['id'])
						cb.to_delete_parser_vars.push(cb.parser_vars[parser_var]['id'])

			$scope.callback.parser_vars = x;
		}
	}

	$scope.deleteRequestVar = function(local_id){
		console.log($scope.initialized);
		if ($scope.initialized == true){
			var cb = $scope.callback;
			console.log('delete request var');

			x = new Array();
			for (request_var in cb.request_vars)
				if (!(cb.request_vars[request_var]['local_id'] == local_id))
					x.push(cb.request_vars[request_var]);
				else
					if (cb.request_vars[request_var]['id'])
						cb.to_delete_request_vars.push(cb.request_vars[request_var]['id'])

			$scope.callback.request_vars = x;
		}
	}

	$scope.deleteCallback = function(){
		if ($scope.callback.id)
			Callback.delete(null, $scope.callback, function(){
				toast("Callback successfully deleted", true);
				window.history.back();
			}, function(){
				toast("Error: Callback could not be deleted", false);
			});
		else {
			window.history.back();
		}
	}

	$scope.scriptSelectChange = function(){
		$http({method: 'GET', url:'/script/' + $scope.callback.script}).success(function(data, status, headers, config){
			if (data.name == $scope.callback.script){
				console.log(data.usage);
				$scope.script_usage = data.usage;
			} else {

			}
		});

	}

	$scope.getCallback = function(){
		var deferred = $q.defer();

		$scope.callback = Callback.get({id: tmpCallbackId},function(){
			var cb = $scope.callback;

			var tmp = cb.last_time;
			cb.to_delete_parser_vars = [];
			cb.to_delete_request_vars = [];

			console.log(cb);
			for (parser_var in cb.parser_vars){
				console.log(parser_var);
				cb.parser_vars[parser_var]['local_id'] = local_parser_id_counter++;
			}

			for (request_var in cb.request_vars){
				console.log(request_var);
				cb.request_vars[request_var]['local_id'] = local_request_id_counter++;
			}

			if (tmp)
				cb.last_time = new Date(tmp[0], tmp[1] - 1, tmp[2], tmp[3], tmp[4], tmp[5]).toString();
			else
				cb.last_time = 'n/a';

			deferred.resolve($scope.callback);
		});

		return deferred.promise;
	};

	$scope.getScripts = function(){
		var deferred = $q.defer();

		$http({method: 'GET', url:'/scripts'}).success(function(data, status, headers, config){
			var cb = $scope.callback;
			x = new Array();
			$scope.script = data.indexOf(cb.script);

			for (a in data)
				x.push(data[a].toString());

			$scope.scripts = {
				"type": "select",
				"value": data[data.indexOf(cb.script)],
				"values": data,
			};
			deferred.resolve({});
		});

		return deferred.promise;
	}

	$scope.toggle = function(){
		$scope.callback.enabled = $scope.callback.enabled < 1 ? 1 : 0;
	}

	// If it has an id that means it exists server-side
	if (tmpCallbackId){
		$scope.getCallback().then(
			function(resolved){
				$scope.getScripts().then(function(scripts){
					$scope.initialized = true;
					$scope.scriptSelectChange();
				});
			});

	} else {
		$scope.callback = new Callback();
		var cb = $scope.callback;
		cb.last_time = 'n/a';
		cb.to_delete_parser_vars = [];
		cb.to_delete_request_vars = [];

		cb.parser_vars = [];
		cb.request_vars = [];

		cb.url="";
		cb.enabled=-1;
		cb.script =
		cb.callbacks_url="";

		$scope.getScripts().then(function(scripts){
			$scope.initialized = true;
		});
	}
});
