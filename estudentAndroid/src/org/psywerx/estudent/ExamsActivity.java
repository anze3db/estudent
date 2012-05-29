package org.psywerx.estudent;

import org.psywerx.estudent.extra.HelperFunctions;
import org.psywerx.estudent.json.EnrollmentExamDates.EnrollmentExamDate;

import android.app.Activity;
import android.app.FragmentTransaction;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

public class ExamsActivity extends Activity implements ExamsFragment.OnExamSelectedListener {
	
	private Context mContext;
	private ExamDetailsFragment mViewer;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exams_fragment);

		mViewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
		mContext = getApplicationContext();
		
		if (mViewer != null && mViewer.isInLayout()) {
			FragmentTransaction ft = getFragmentManager().beginTransaction();
			ft.hide(mViewer);
			ft.commit();
		}
	}
	
	public void onExamSelected(int action) {
		EnrollmentExamDate e = StaticData.mEnrollmentExamDates.get(action);
		if (mViewer == null || !mViewer.isInLayout()) {
    		Intent showContent = new Intent(mContext, ExamDetailsActivity.class);
    		showContent.putExtra("id", ""+e.exam_key);
    		showContent.putExtra("name", e.course);
    		showContent.putExtra("teacher", e.instructors);
    		showContent.putExtra("date", HelperFunctions.dateToSlo(e.date));
            startActivity(showContent);
    	} else {
			if(mViewer.isHidden()) {
				FragmentTransaction ft = getFragmentManager().beginTransaction();
				ft.setCustomAnimations(android.R.animator.fade_in, android.R.animator.fade_out);
				ft.show(mViewer);
				ft.commit();
			}
    		mViewer.showData(""+e.exam_key, e.course, e.instructors, HelperFunctions.dateToSlo(e.date));
    	}
	}
	
	
}
