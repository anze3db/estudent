package org.psywerx.estudent.json;

import java.io.Serializable;
import java.util.List;

public class EnrollmentExamDates {
	
	public class EnrollmentExamDate implements Serializable {
		private static final long serialVersionUID = 1L;
		public int attempts_this_year;
		public int repeat_class_exams;
		public int all_attempts;
		public int exam_key;
		public int course_code;
		public String date;
		public String instructors;
		public String course;
		public boolean signedup;
	}
	public List<EnrollmentExamDate> EnrollmentExamDates;
}
