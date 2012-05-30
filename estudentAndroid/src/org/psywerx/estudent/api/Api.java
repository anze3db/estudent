package org.psywerx.estudent.api;

import org.psywerx.estudent.json.EnrollmentExamDates;
import org.psywerx.estudent.json.Signup;
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
	
	public static void applyExam(ResponseListener rl,String exam_id, String studnet_id, String enroll_id) {
		String apiSubDirectory = "addSignUp/";
		RequestAsyncTask task = new RequestAsyncTask(rl,apiSubDirectory,Signup.class);
		task.execute("student_id", studnet_id, "exam_id", exam_id, "enroll_id", enroll_id);
	}
	
	public static void unapplyExam(ResponseListener rl, String un, String key) {
		String apiSubDirectory = "removeSignUp/";
		RequestAsyncTask task = new RequestAsyncTask(rl,apiSubDirectory,Signup.class);
		task.execute("student_id",un, "exam_id", key);
	}
}
