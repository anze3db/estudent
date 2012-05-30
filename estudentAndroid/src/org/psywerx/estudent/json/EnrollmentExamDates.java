package org.psywerx.estudent.json;

import java.io.Serializable;
import java.util.List;

public class EnrollmentExamDates {
	
	public class EnrollmentExamDate implements Serializable {
		private static final long serialVersionUID = 1L;
		public String date;
		public int exam_key;
		public String instructors;
		public String course;
		public boolean signedup;
	}
	public List<EnrollmentExamDate> EnrollmentExamDates;
}
