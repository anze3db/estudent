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
	private ExamsFragment mViewer;
	private ExamDetailsFragment mDetailsViewer;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exams_fragment);

		mViewer = (ExamsFragment) getFragmentManager().findFragmentById(R.id.examsFragment);
		mDetailsViewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
		
		mContext = getApplicationContext();
		
		if (mDetailsViewer != null && mDetailsViewer.isInLayout()) {
			mDetailsViewer.setmSignListener(mViewer);
			FragmentTransaction ft = getFragmentManager().beginTransaction();
			ft.hide(mDetailsViewer);
			ft.commit();
		}
		
		setTitle(String.format("%s %s (%s)", StaticData.username, StaticData.lastName, StaticData.username));
	}
	
	public void onExamSelected(int action) {
		EnrollmentExamDate e = StaticData.mEnrollmentExamDates.get(action);
		if (mDetailsViewer == null || !mDetailsViewer.isInLayout()) {
    		Intent showContent = new Intent(mContext, ExamDetailsActivity.class);
    		showContent.putExtra("id", ""+e.exam_key);
    		showContent.putExtra("name", e.course);
    		showContent.putExtra("teacher", e.instructors);
    		showContent.putExtra("date", HelperFunctions.dateToSlo(e.date));
    		showContent.putExtra("signedup", e.signedup);
            startActivity(showContent);
    	} else {
			if(mDetailsViewer.isHidden()) {
				FragmentTransaction ft = getFragmentManager().beginTransaction();
				ft.setCustomAnimations(android.R.animator.fade_in, android.R.animator.fade_out);
				ft.show(mDetailsViewer);
				ft.commit();
			}
    		mDetailsViewer.showData(""+e.exam_key, e.course, e.instructors, HelperFunctions.dateToSlo(e.date), e.signedup);
    	}
	}
	
	@Override
	protected void onResume() {
		mViewer.reloadData();
		super.onResume();
	}
	
}
