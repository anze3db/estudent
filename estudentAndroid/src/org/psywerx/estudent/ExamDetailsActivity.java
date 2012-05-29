package org.psywerx.estudent;

import android.app.Activity;
import android.os.Bundle;

public class ExamDetailsActivity extends Activity {
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exam_details_fragment);
		
		Bundle extras = getIntent().getExtras();
	    ExamDetailsFragment viewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
	    viewer.showData(extras.getString("id"), extras.getString("name"), extras.getString("teacher"), extras.getString("date"), extras.getBoolean("signedup"));
	}

}
