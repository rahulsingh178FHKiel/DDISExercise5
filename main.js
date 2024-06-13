import http from 'k6/http';
import { URLSearchParams } from 'https://jslib.k6.io/url/1.0.0/index.js';
import { sleep } from 'k6';

const URL = 'https://python-flask-bzm6f2c6ga-ew.a.run.app'
// const URL = 'http://127.0.0.1:5000';


export default function () {

    console.log('In main function');

    // get 1 random email and password for the current user
    const [email, password] = get1row();


    const [selfuid, loginHeaders] = loginAndGetOwnUserDetails(email, password);



    const allActions = [listOwnSales, listOwnPurchases, createoffer, listOffersAndBuyFirstExistingOffer, offerbyuseridAndDeleteFirstIfExists];
    const selectedActions = [];

    while (selectedActions.length < 3) {
        const randomIndex = Math.floor(Math.random() * allActions.length);
        selectedActions.push(allActions[randomIndex]);
    }

    // Execute the selected actions

    selectedActions.forEach((action) => {
        action(selfuid, loginHeaders);
        const actualThinkTime = simulateThinkTime(1, 0.5); // Mean: 1000 ms, StdDev: 500 ms
        console.log(" Sleep time "+actualThinkTime+"s");
    	sleep(actualThinkTime)
    });


    checkIfTotalBalanceIsZero();

}

console.log("Load test is complete.");

function generateRandomNormal(mean, stdDev) {
    const u1 = Math.random();
    const u2 = Math.random();

    // Apply the Box-Muller transform
    const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);

    // Scale and shift to match the desired mean and standard deviation
    const randomValue = mean + stdDev * z0;

    return randomValue;
}

function simulateThinkTime(mean, stdDev) {
    const thinkTime = generateRandomNormal(mean, stdDev);
    return thinkTime;
}

function get1row() {

	const url = URL+'/get1row';

    const uidresponse = http.get(url);

    const uidresponseBody = JSON.parse(uidresponse.body);

    const email = uidresponseBody.email;

    const password = uidresponseBody.password;

    return [email, password];

}


function checkIfTotalBalanceIsZero() {

	//case 11
	
    const url = URL+'/getbalancesum';

    const uidresponse = http.get(url);

    const uidresponseBody = JSON.parse(uidresponse.body);

    const balanceSum = uidresponseBody.balanceSum;

    // console.log("Case 11 balanceSum : ", balanceSum)

    if (balanceSum != 0) {
    	console.log("ERROR : The balance was not found to be zero."); }
    else
    	{console.log("Total balance was found to be zero.");}
}

function listOwnSales(uid, headers) {

	//case 3
	const queryParams = new URLSearchParams([
        ['user_id', uid],
    ]);

    const url = URL+'/saleoffers?'+queryParams.toString()+'&item_title=&manufacturer_description=&seller_description=';

    const uidresponse = http.get(url, headers);

    const uidresponseBody = JSON.parse(uidresponse.body);

    console.log("Case 3")


}

function listOwnPurchases(uid, headers) {


	//case 4 
	const queryParams = new URLSearchParams([
        ['user_id', uid],
    ]);

    const url = URL+'/purchaseoffers?'+queryParams.toString()+'&item_title=&manufacturer_description=&seller_description=';

    const uidresponse = http.get(url, headers);

    const uidresponseBody = JSON.parse(uidresponse.body);

    console.log("Case 4")


}


function createoffer(selfuid, headers) {

	//case 7

    const url = URL+'/createoffer';

    const uidresponse = http.put(url, {}, headers);

    const uidresponseBody = JSON.parse(uidresponse.body);

    console.log("Case 7")

}

function listOffersAndBuyFirstExistingOffer(uid, headers) {

	//case 6 and 8 mix

    const url = URL+'/offerby100users';

    const uidresponse = http.get(url, headers);

    const uidresponseBody = JSON.parse(uidresponse.body);

    console.log("Case 6")

    if (Array.isArray(uidresponseBody) && uidresponseBody.length > 0) {
        const firstElement = uidresponseBody[0];
        // console.log('First element:', firstElement);
        const sale_id = firstElement[0];
        // console.log("sale_id "+sale_id);

        const queryParamsdeleteOffercase = new URLSearchParams([
        ['sale_id', sale_id],
    ]);

    const buyOfferUrl = URL+'/buyofferbysaleid?'+queryParamsdeleteOffercase.toString();

    const buyOfferuidresponse = http.put(buyOfferUrl, null, headers);

    const buyOfferuidresponseBody = JSON.parse(buyOfferuidresponse.body);

    console.log("Case 8");

    } else {
        console.log('No item was found.');
    }

}

function offerbyuseridAndDeleteFirstIfExists(uid, headers) {

	//case 5 and 9 mixed

	const queryParams = new URLSearchParams([
        ['user_id', uid],
    ]);

    const url = URL+'/offerbyuserid?'+queryParams.toString();

    const uidresponse = http.get(url, headers);
	const uidresponseBody = JSON.parse(uidresponse.body);

    
     if (Array.isArray(uidresponseBody) && uidresponseBody.length > 0) {
        const firstElement = uidresponseBody[0];
        console.log('First element:', firstElement);
        const sale_id = firstElement[0];
        const queryParamsdeleteOffercase = new URLSearchParams([
        ['sale_id', sale_id],
    ]);

    const deleteOfferUrl = URL+'/deleteofferbysaleid?'+queryParamsdeleteOffercase.toString();

    const deleteOfferuidresponse = http.del(deleteOfferUrl, null, headers);

    const deleteOfferuidresponseBody = JSON.parse(deleteOfferuidresponse.body);

    console.log("Case 9");

    } else {
        console.log('No data or empty array in the response.');
    }


}

function callActionsRandomly(selfuid, loginHeaders) {
	
		// const allActions = [listOwnSales, listOwnPurchases, createoffer, listOffersAndBuyFirstExistingOffer, offerbyuseridAndDeleteFirstIfExists];
	const allActions = [listOwnSales, createoffer, listOffersAndBuyFirstExistingOffer, offerbyuseridAndDeleteFirstIfExists];
		const selectedActions = [];

		while (selectedActions.length < 3) {
		    const randomIndex = Math.floor(Math.random() * allActions.length);
		    selectedActions.push(allActions[randomIndex]);
		}

		// Execute the selected actions

		selectedActions.forEach((action) => {
		    action(selfuid, loginHeaders);
		    const actualThinkTime = simulateThinkTime(1000, 500); // Mean: 1000 ms, StdDev: 500 ms
			sleep(actualThinkTime);
		});

}



function loginAndGetOwnUserDetails(email, password) {
    
	// Query 1: Login

    const loginurl = URL+'/login'; 
   
    const payload = JSON.stringify({
        email: email,
        password: password,
    });
    
    const headers = {
        'Content-Type': 'application/json',
    };
    
    const response = http.post(loginurl, payload, { headers });

    const responseBody = JSON.parse(response.body);
    
    const token = responseBody.token;

    // Query 2 : Get own user id

    const getownuseridURL = URL+'/getownuserid';

    const loginHeaders = {
    headers: {
        Authorization: `Bearer ${token}`,
             },
    };

    const uidresponse = http.get(getownuseridURL, loginHeaders);

    const uidresponseBody = JSON.parse(uidresponse.body);

    const selfuid = uidresponseBody.uid;
    
    // Query 3 : Get details of user with the user id

     const queryParams = new URLSearchParams([
        ['user_id', selfuid],
    ]);

    const getOwnUserDetailsURL = URL+'/userinfo?'+ queryParams.toString();

    const getOwnUserDetailsuidresponse = http.get(getOwnUserDetailsURL, loginHeaders);

    const getOwnUserDetailsuidresponseBody = JSON.parse(getOwnUserDetailsuidresponse.body);

    return [selfuid, loginHeaders];

}