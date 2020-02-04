(function(angular) {
    let app = angular.module("app");

    app.controller("DetailsCtrl", [
        "$http",
        "$scope",
        "$state",
        "$stateParams",
        function($http, $scope, $state, $stateParams) {
            let that = this;

            $scope.myInterval = 5000;
            $scope.noWrapSlides = false;
            $scope.active = 0;
            $scope.isReadonly = true;

            this.selectedAccommodation = {
                accommodation_types_id: null,
                cities_id: null,
                name: "",
                price_per_night: null,
                stars: null,
                street_address: "",
                description: "",
                breakfast: null,
                internet: null,
                available: null
            };

            this.newReservation = {
                accommodation_id: null,
                users_id: null,
                nights: null,
                date: "",
                total_price: 0
            };

            $scope.dt = new Date();

            this.nights = 1;

            this.images = [];
            this.filteredImages = [];

            this.calculateTotal = function() {
                that.newReservation.total_price =
                    that.selectedAccommodation.price_per_night * that.newReservation.nights;
            };

            this.getUser = function() {
                $http.get("api/user").then(
                    function(response) {
                        console.log(response);
                        that.newReservation.users_id = response.data.id;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAccommodation = function() {
                $http.get("api/accommodation/details/" + $stateParams["id"]).then(
                    function(response) {
                        console.log(response);
                        that.selectedAccommodation = response.data;
                        that.newReservation.accommodation_id = response.data.id;
                        that.getImages();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.makeReservation = function() {
                $http.post("api/accommodation/reservation", that.newReservation).then(
                    function(response) {
                        console.log(response);
                        $state.go("dashboard.reservations_and_tickets");
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getImages = function() {
                $http.get("api/accommodation/images").then(
                    function(response) {
                        console.log(response);
                        this.images = response.data;

                        for (let image of images) {
                            if (that.selectedAccommodation.name == image.name) {
                                that.filteredImages.push(image.path);
                            }
                        }
                        console.log(that.filteredImages);
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAccommodation();
            this.calculateTotal();
            this.getUser();
        }
    ]);
})(angular);
