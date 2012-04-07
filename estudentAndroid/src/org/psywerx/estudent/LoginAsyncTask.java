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


class LoginAsyncTask extends AsyncTask<String, Void, User> {

	private static final String SERVER_URL = "www.zidar.me/user.json";
	
	/**
	 * Class constructor 
	 */
	protected LoginAsyncTask() {
	}

	protected User doInBackground(String... userData) {
		User result = null;
		try{
			if (userData.length == 2){
				result = verifyLogin(userData[0],userData[1]);
			}
		} catch (Exception e) {
			//error in fetch service should not effect the application at all !
			D.dbge(e.toString());
			result = null;
		}
		return result;
	}


	private User verifyLogin(String username,String password){
		User user = null;
		try {
			String requestUrl = (SERVER_URL+"?"+
					HelperFunctions.getFetchParams(
							"action","verifyLogin",
							"username",username,
							"password",password)
					);

			String responseString = fetchGetRequest(requestUrl);
			Gson g = new Gson();
			if (!"".equals(responseString) && responseString != null){
				user = (User) g.fromJson(responseString, User.class);
			}

		} catch (ClientProtocolException e){
			D.dbge(e.toString());
		} catch (IOException e){
			D.dbge(e.toString());
		} catch (Exception e){
			D.dbge(e.toString(),e);
		}
		return user;
	}

	private String fetchGetRequest(String url) throws ClientProtocolException, IOException{
		HttpClient httpclient = new DefaultHttpClient();
		HttpResponse response;
		String responseString = null;
		response = httpclient.execute(new HttpGet(url));
		StatusLine statusLine = response.getStatusLine();
		if(statusLine.getStatusCode() == HttpStatus.SC_OK){
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

	protected void onPostExecute(User result) {
		D.dbgv("ime: "+result.getFirstname());
		D.dbgv("priimek: "+result.getLastname());
	}
}

