package org.psywerx.estudent.api;

import org.psywerx.estudent.json.EnrollmentExamDates;
import org.psywerx.estudent.json.StudentEnrollments;
import org.psywerx.estudent.json.User;

public class Api {
	public static void loginRequest(ResponseListener rl, String un, String ps){
		String apiSubDirectory = "login/";
		RequestAsyncTask task = new RequestAsyncTask(rl,apiSubDirectory,User.class);
		task.execute("id",un,"password",ps);
	}
	
	public static void studentEnrollmentsRequest(ResponseListener rl, String un) {
		String apiSubDirectory = "getStudentEnrollments/";
		RequestAsyncTask task = new RequestAsyncTask(rl,apiSubDirectory,StudentEnrollments.class);
		task.execute("student_id",un);
	}
	
	public static void enrollmentExamDatesRequest(ResponseListener rl, String key) {
		String apiSubDirectory = "getEnrollmentExamDates/";
		RequestAsyncTask task = new RequestAsyncTask(rl,apiSubDirectory,EnrollmentExamDates.class);
		task.execute("enroll_id",key);
	}
}
