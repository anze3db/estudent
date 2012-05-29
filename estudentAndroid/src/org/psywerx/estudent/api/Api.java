package org.psywerx.estudent.api;

import org.psywerx.estudent.api.RequestAsyncTask;
import org.psywerx.estudent.json.StudentEnrollments;
import org.psywerx.estudent.json.User;

public class Api {
	public static void loginRequest(ResponseListener rl, String un, String ps){
		String apiSubDirectory = "login/";
		RequestAsyncTask loginTask = new RequestAsyncTask(rl,apiSubDirectory,User.class);
		loginTask.execute("id",un,"password",ps);
	}
	
	public static void examListRequest(ResponseListener rl, String un) {
		String apiSubDirectory = "getStudentEnrollments/";
		RequestAsyncTask examTask = new RequestAsyncTask(rl,apiSubDirectory,StudentEnrollments.class);
		examTask.execute("student_id",un);
	}
}
