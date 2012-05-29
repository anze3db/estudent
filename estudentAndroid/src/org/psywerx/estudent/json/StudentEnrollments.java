package org.psywerx.estudent.json;

import java.util.List;

public class StudentEnrollments {
	class StudentEnrolment {
		public int study_year;
		public int class_year;
		public int key;
		public String study_program;
	}
	public List<StudentEnrolment> enrollments;
}
