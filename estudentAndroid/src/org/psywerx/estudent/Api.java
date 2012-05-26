package org.psywerx.estudent;

import org.psywerx.estudent.api.RequestAsyncTask;

public class Api {
	protected static void loginRequest(ResponseListener rl, String un, String ps){
		String apiSubDirectory = "login/";
		RequestAsyncTask loginTask = new RequestAsyncTask(rl,apiSubDirectory);
		loginTask.execute("id",un,"password",ps);
	}
}
