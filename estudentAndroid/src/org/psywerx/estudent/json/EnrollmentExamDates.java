package org.psywerx.estudent.json;

import java.util.List;

public class EnrollmentExamDates {
	public class EnrollmentExamDate {
		public String date;
		public int exam_key;
		public String instructors;
		public String course;
	}
	public List<EnrollmentExamDate> EnrollmentExamDates;
}
