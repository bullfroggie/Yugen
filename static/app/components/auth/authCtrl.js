(function(angular) {
	let app = angular.module("app");

	app.controller("AuthCtrl", [
		"$scope",
		"$state",
		"$http",
		function($scope, $state, $http) {
			let that = this;

			$scope.alerts = [];

			$scope.addAlert = function(message) {
				$scope.alerts.push(message);
			};

			$scope.closeAlert = function(index) {
				$scope.alerts.splice(index, 1);
			};

			this.newUser = {
				user_type: 2,
				first_name: "",
				last_name: "",
				username: "",
				password: "",
				date_of_birth: "",
				email: "",
				profile_image: "styles/images/regular_user_icon.png", // default profile image
				active: 1
			};

			this.registerUser = function() {
				$http.post("api/user/registration", that.newUser).then(
					function(response) {
						console.log(response);
						$state.go("login");
					},
					function(reason) {
						console.log(reason);
						if (reason.status == 409) {
							$scope.addAlert({
								type: "danger",
								msg: "Username already exists! Try slightly altering it.."
							});
						}
					}
				);
			};
		}
	]);
})(angular);
