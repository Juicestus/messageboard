/*
 * Sign Up Client Side
 * (c) Justus Languell 2020-2021
 */

illegalCharsMsg = ' can only use the English alphabet, digits 0-9, underscore, and period!'
legalChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.'

function isLegal(s,l)
{
    legal = true;

    for (var i=0; i<l; i++)
    {
        charLegal = false;

        if (!legalChars.includes(s[i]))
        {        
            legal = false;
        };
    };
    
    return legal;
};


$(document).ready(function() 
{
    var username = document.getElementById('username');
    var password = document.getElementById('password');
    var confirm = document.getElementById('confirm');


    username.addEventListener('input', function usernameSafe(e)
    {
        var field = e.target;
        var legal = isLegal(field.value, field.value.length);

        if (!legal)
        {
            document.getElementById('usernameError').innerHTML = 'Username' + illegalCharsMsg;
        }
        else
        {
            document.getElementById('usernameError').innerHTML = '';
        }
    });

    password.addEventListener('input', function passnameSafe(e)
    {
        var field = e.target;
        var legal = isLegal(field.value, field.value.length);

        if (!legal)
        {
            document.getElementById('passwordError').innerHTML = 'Password' + illegalCharsMsg;
        }
        else
        {
            document.getElementById('passwordError').innerHTML = '';
        }
    });

    confirm.addEventListener('input', function confnameSafe(e)
    {
        var field = e.target;
        var legal = isLegal(field.value, field.value.length);

        if (!legal)
        {
            document.getElementById('confirmError').innerHTML = 'Confirm' + illegalCharsMsg;
        }
        else
        {
            document.getElementById('confirmError').innerHTML = '';
        }
    });



});



setInterval(function()
{
    var submit = document.getElementById('submit');

    submit.disabled = (
    (document.getElementById('usernameError').innerHTML != '')||
    (document.getElementById('passwordError').innerHTML != '')||
    (document.getElementById('confirmError').innerHTML != ''));

    ;
},
10);