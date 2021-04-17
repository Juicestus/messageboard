/*
 * Tests for client side encryption
 * (c) Justus Languell 2020-2021
 */

$(document).ready(function() 
{
    var formElem = document.getElementById('regForm')
    //function (e)
    formElem.onsubmit = async (e) => 
    {
        e.preventDefault();


        let formData = new FormData(formElem);

        var fusername = formData.get('username');
        var fpassword = formData.get('password');
        var fconfirm = formData.get('confirm');

        formData.set('password', sha256(fusername + fpassword));
        formData.set('confirm', sha256(fusername + fconfirm));


        var request = new XMLHttpRequest();
        request.open("POST", "/signup");
        request.send(formData);

        /*let response = await fetch('/signup', {
            method: 'POST',
            headers: new Headers({
                //'Content-Type': 'application/x-www-form-urlencoded'
                'Content-Type': 'application/json'
            }),
            body: formData
        });*/
        //window.location.replace("/");

    };
});