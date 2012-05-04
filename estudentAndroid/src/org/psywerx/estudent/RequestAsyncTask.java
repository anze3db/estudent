package org.psywerx.estudent;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.psywerx.estudent.json.User;

import android.os.AsyncTask;

import com.google.gson.Gson;



class RequestAsyncTask extends AsyncTask<String, Void, Object> {

	private static final String SERVER_URL = "http://192.168.1.4/api/";
	private String mApiSubDir = "";
	
	private ResponseListener responseListener;

	/**
	 * Class constructor 
	 */
	protected RequestAsyncTask(ResponseListener r) {
		responseListener = r;
	}
	/**
	 * Class constructor 
	 */
	protected RequestAsyncTask(ResponseListener r, String apiClass) {
		responseListener = r;
		mApiSubDir = apiClass;
	}

	protected Object doInBackground(String... data) {
		Object result = null;
		try{
			String requestUrl = (SERVER_URL+mApiSubDir+"?"+HelperFunctions.getFetchParams(data));

			String responseString = fetchGetRequest(requestUrl);
			D.dbgv("response String: "+responseString);
			
			Gson g = new Gson();
			if (!"".equals(responseString) && responseString != null){
				result =  g.fromJson(responseString, User.class);
			}
		} catch (Exception e) {
			//error in fetch service should not effect the application at all !
			D.dbge(e.toString());
			result = null;
		}
		return result;
	}

	private String fetchGetRequest(String url) throws ClientProtocolException, IOException{
		HttpClient httpclient = new DefaultHttpClient();
		HttpResponse response;
		String responseString = null;
		D.dbgv("sending request: "+url);
		response = httpclient.execute(new HttpGet(url));
		StatusLine statusLine = response.getStatusLine();
		if(statusLine.getStatusCode() == HttpStatus.SC_OK){
			D.dbgv("recieved response: "+statusLine.getStatusCode());
			ByteArrayOutputStream out = new ByteArrayOutputStream();
			response.getEntity().writeTo(out);
			out.close();
			responseString = out.toString();
		} else{
			//Closes the connection.
			response.getEntity().getContent().close();
			throw new IOException(statusLine.getReasonPhrase());
		}
		return responseString;
	}

	protected void onPostExecute(Object result) {
		if (result != null){
			responseListener.onServerResponse(result);
		}else{
			D.dbge("result is null");
		}
	}
}

