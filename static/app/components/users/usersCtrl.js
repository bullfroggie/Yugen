(function(angular) {
    let app = angular.module("app");

    app.controller("UsersCtrl", ["$http", function($http) {
        let that = this;
        let date = new Date().toJSON().slice(0,10).replace(/-/g,'-');

        this.users = [];
        this.newUser = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "password": "",
            "date_of_birth": date,
            "email": "",
            "profile_image": ""
        };

        this.getUsers = function() {

            $http.get("api/users").then(function(result) {
                console.log(result);
                that.users = result.data;
            }, function(reason) {
                console.log(reason);
            });
        }

        this.getUsers();
    }]);
})(angular);