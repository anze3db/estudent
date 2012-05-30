package org.psywerx.estudent;

import org.psywerx.estudent.json.EnrollmentExamDates.EnrollmentExamDate;

import android.app.Activity;
import android.os.Bundle;

public class ExamDetailsActivity extends Activity {
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exam_details_fragment);
		
		Bundle extras = getIntent().getExtras();
	    ExamDetailsFragment viewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
	    viewer.setExam((EnrollmentExamDate) extras.getSerializable("examId"));
	    viewer.showData();
	}

}
