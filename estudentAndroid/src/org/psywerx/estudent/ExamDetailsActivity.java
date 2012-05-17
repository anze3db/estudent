package org.psywerx.estudent;

import android.app.Activity;
import android.os.Bundle;

public class ExamDetailsActivity extends Activity {
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exam_details_fragment);
		
//		Intent launchingIntent = getIntent();
	    ExamDetailsFragment viewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
	    viewer.showData("", "", "", "");
	}

}
