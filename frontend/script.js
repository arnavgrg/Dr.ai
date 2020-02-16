import "houndify"

//HTML ELEMENTS FOR DISPLAYING RESPONSE AND INFO JSON's
const responseElt = document.getElementById("responseJSON");
const infoElt = document.getElementById("infoJSON");
const statusElt = document.getElementById("status");
const transcriptElt = document.getElementById("query");
const voiceIcon = document.getElementById("voiceIcon");

// UPDATE YOUR CLIENT ID HERE TO YOUR HOUNDIFY.COM CLIENT ID.
const clientID =  "94iXzZrdKCISkoWU-y1teQ==";
let conversationState = null;
let voiceRequest = null;

const recorder = new Houndify.AudioRecorder();
recorder.on("start", function() {
    //Initialize VoiceRequest
    voiceRequest = initVoiceRequest(recorder.sampleRate);
    voiceIcon.classList.replace("bg-black", "bg-red-700");
});

recorder.on("data", function(data) {
    voiceRequest.write(data);
});

recorder.on("end", function() {
    voiceRequest.end();
    statusElt.innerText = "Stopped recording. Waiting for response...";

    voiceIcon.classList.replace("bg-red-700", "bg-black");
    document.getElementById("textSearchButton").disabled = false;
    document.getElementById("query").readOnly = false;
});

recorder.on("error", function(error) {
    voiceRequest.abort();
    statusElt.innerText = "Error: " + error;
    voiceIcon.classList.replace("bg-red-700", "bg-black");
    document.getElementById("textSearchButton").disabled = false;
    document.getElementById("query").readOnly = false;
});

function initTextRequest() {
    responseElt.parentNode.hidden = true;
    infoElt.parentNode.hidden = true;

    const queryString = document.getElementById("query").value;
    statusElt.innerText = "Sending text request...";

    //Initialize TextRequest
    const textRequest = new Houndify.TextRequest({
	//Text query
	query: queryString,

	//Your Houndify Client ID
	clientId: clientID,

	//For testing environment you might want to authenticate on frontend without Node.js server.
	//In that case you may pass in your Houndify Client Key instead of "authURL".
	clientKey: "_7OwfiGjU6q8ppWY5NuP7AikDNt9JQo02ke3nNv39leZNz8DPwxZyOOO9Oh6ErMrvRKv8NFk_aOPiUhfQ4kxIA==",

	//Otherwise you need to create an endpoint on your server
	//for handling the authentication.
	//See SDK's server-side method HoundifyExpress.createAuthenticationHandler().
	//{#authURL: "/houndifyAuth",#}

	//REQUEST INFO JSON
	//See https://houndify.com/reference/RequestInfo
	requestInfo: {
	    UserID: "test_user",
	    Latitude: 37.388309,
	    Longitude: -121.973968
	},

	//Pass the current ConversationState stored from previous queries
	//See https://www.houndify.com/docs#conversation-state
	conversationState: conversationState,

	//You need to create an endpoint on your server
	//for handling the authentication and proxying
	//text search http requests to Houndify backend
	//See SDK's server-side method HoundifyExpress.createTextProxyHandler().
	proxy: {
	    method: "POST",
	    //url: "/textSearchProxy", 
	    headers: {
		"Access-Control-Allow-Origin": "http://localhost:5000"
	    }
	    // .. More proxy options will be added as needed
	},

	//Response and error handlers
	onResponse: onResponse,
	onError: onError
    });
}

function initVoiceRequest(sampleRate) {
    responseElt.parentNode.hidden = true;
    infoElt.parentNode.hidden = true;

    const voiceRequest = new Houndify.VoiceRequest({
	//Your Houndify Client ID
	clientId: clientID,

	//For testing environment you might want to authenticate on frontend without Node.js server.
	//In that case you may pass in your Houndify Client Key instead of "authURL".
	clientKey: "_7OwfiGjU6q8ppWY5NuP7AikDNt9JQo02ke3nNv39leZNz8DPwxZyOOO9Oh6ErMrvRKv8NFk_aOPiUhfQ4kxIA==" ,

	//Otherwise you need to create an endpoint on your server
	//for handling the authentication.
	//See SDK's server-side method HoundifyExpress.createAuthenticationHandler().
	authURL: "/houndifyAuth",

	//REQUEST INFO JSON
	//See https://houndify.com/reference/RequestInfo
	requestInfo: {
	    UserID: "test_user",
	    Latitude: 37.388309,
	    Longitude: -121.973968
	},

	//Pass the current ConversationState stored from previous queries
	//See https://www.houndify.com/docs#conversation-state
	conversationState: conversationState,

	//Sample rate of input audio
	sampleRate: sampleRate,

	//Enable Voice Activity Detection
	//Default: true
	enableVAD: true,

	//Partial transcript, response and error handlers
	onTranscriptionUpdate: onTranscriptionUpdate,
	onResponse: function(response, info) {
	    recorder.stop();
	    onResponse(response, info);
	},
	onError: function(err, info) {
	    recorder.stop();
	    onError(err, info);
	}
    });

    return voiceRequest;
}

function onMicrophoneClick() {
    if (recorder && recorder.isRecording()) {
	recorder.stop();
	return;
    }

    recorder.start();

    statusElt.innerText = "Streaming voice request...";
    voiceIcon.classList.replace("bg-black", "bg-red-700");
    document.getElementById("textSearchButton").disabled = true;
    document.getElementById("query").readOnly = true;
}

function onFileUpload() {
    const reader = new FileReader();
    reader.onload = function() {
	//In browsers only you can also upload and decode
	//audio file using decodeArrayBuffer() method
	//Stream 8/16 kHz mono 16-bit little-endian PCM samples
	//in Int16Array() chunks to backend
	const arrayBuffer = reader.result;
	Houndify.decodeAudioData(arrayBuffer, function(err, result) {
	    statusElt.innerText = "Streaming audio from file...";
	    voiceRequest = initVoiceRequest(result.sampleRate);
	    voiceRequest.write(result.audioData);
	    voiceRequest.end();
	});

	statusElt.innerText = "Decoding audio from file...";
    };

    const file = document.getElementById("file").files[0];
    reader.readAsArrayBuffer(file);
}

function fireEvent(data) {
    console.log(data)
}

//Fires after server responds with Response JSON
//Info object contains useful information about the completed request
//See https://houndify.com/reference/HoundServer
function onResponse(response, info) {
    fireEvent(response.Disambiguation.ChoiceData[0].Transcription)
    if (response.AllResults && response.AllResults.length) {
	//Pick and store appropriate ConversationState from the results.
	//This example takes the default one from the first result.
	conversationState = response.AllResults[0].ConversationState;
    }

    statusElt.innerText = "Received response.";
    responseElt.parentNode.hidden = false;
    responseElt.value = response.stringify(undefined, 2);
    infoElt.parentNode.hidden = false;
    infoElt.value = JSON.stringify(info, undefined, 2);
}

//Fires if error occurs during the request
function onError(err, info) {
    statusElt.innerText = "Error: " + JSON.stringify(err);
    responseElt.parentNode.hidden = true;
    infoElt.parentNode.hidden = false;
    infoElt.value = JSON.stringify(info, undefined, 2);
}

//Fires every time backend sends a speech-to-text
//transcript of a voice query
//See https://houndify.com/reference/HoundPartialTranscript
function onTranscriptionUpdate(transcript) {
    transcriptElt.value = transcript.PartialTranscript;
}
