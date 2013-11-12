angular.module('mypseudoApp',[
	'ngResource',
	'mypseudoApp.controllers'
]).
config(['$routeProvider',
	function($routeProvider){
		$routeProvider.when('/', {
			templateUrl: '/static/partials/list.html',
			controller: 'ListCtrl'
		}).when('/edit/:callback_id',{
			templateUrl: '/static/partials/edit.html',
			controller: 'EditCtrl'
		}).when('/create/',{
			templateUrl: '/static/partials/edit.html',
			controller: 'EditCtrl'
		}).otherwise({
			redirectTo: '/'
		});
	}
]);