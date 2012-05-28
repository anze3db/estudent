package org.psywerx.estudent.api;

import org.psywerx.estudent.api.RequestAsyncTask;

public class Api {
	public static void loginRequest(ResponseListener rl, String un, String ps){
		String apiSubDirectory = "login/";
		RequestAsyncTask loginTask = new RequestAsyncTask(rl,apiSubDirectory);
		loginTask.execute("id",un,"password",ps);
	}
}
