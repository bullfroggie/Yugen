(function(angular) {
    let app = angular.module("app");

    app.controller("AuthCtrl", ["$state", "$http", function($state, $http) {
        let that = this;

        this.newUser = {
            user_type: 2,
            first_name: "",
            last_name: "",
            username: "",
            password: "",
            date_of_birth: "",
            email: "",
            profile_image: ""
        };
    }]);
})(angular);