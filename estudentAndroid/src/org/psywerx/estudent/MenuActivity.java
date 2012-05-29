package org.psywerx.estudent;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
import org.psywerx.estudent.json.EnrollmentExamDates;
import org.psywerx.estudent.json.EnrollmentExamDates.EnrollmentExamDate;
import org.psywerx.estudent.json.StudentEnrollments;
import org.psywerx.estudent.json.StudentEnrollments.StudentEnrollment;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.Menu;
import android.view.View;
import android.widget.ListView;
import android.widget.Toast;

public class MenuActivity extends ListActivity implements ResponseListener{
	
	private Context mContext;
	
	private static final int ACTION_LOGOUT = 0;
	private static final int ACTION_DISPLAY_MY_EXAMS = 1;
	private static final int ACTION_DISPLAY_ALL_EXAMS = 2;
		
	private MenuAdapter mMenuAdapter;
	private ProgressDialog mProgressDialog = null;
	
	private HashMap<Integer, String> mEnrollments = new HashMap<Integer, String>();
		
	private ResponseListener mListener;
	
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mContext = getApplicationContext();
		mListener = (ResponseListener) this;

		List<MenuItem> items = new ArrayList<MenuItem>();
		items.add(new MenuItem(
				getString(R.string.logout_name), 
				getString(R.string.logout_desc),  
				ACTION_LOGOUT, R.drawable.logout_icon_128));
		items.add(new MenuItem(
				getString(R.string.applied_exams_name), 
				getString(R.string.applied_exams_desc), 
				ACTION_DISPLAY_MY_EXAMS, R.drawable.notepad_icon_128));
		items.add(new MenuItem(
				getString(R.string.all_exams_list_name), 
				getString(R.string.all_exams_list_desc), 
				ACTION_DISPLAY_ALL_EXAMS, R.drawable.notepad_icon_128));
		
		mMenuAdapter = new MenuAdapter(mContext, items);
		setListAdapter(mMenuAdapter);
		registerForContextMenu(getListView());
		
		setTitle(String.format("%s %s (%s)", StaticData.username, StaticData.lastName, StaticData.username));
	}
	
	@Override
	protected void onListItemClick(ListView l, View v, int position, long id) {
		super.onListItemClick(l, v, position, id);
		switch (mMenuAdapter.getItem(position).getAction()) {
		case ACTION_DISPLAY_MY_EXAMS:
			mProgressDialog = ProgressDialog.show(MenuActivity.this,    
					getString(R.string.loading_please_wait), 
					getString(R.string.loading_verifying_login), true);
			Api.studentEnrollmentsRequest(mListener, StaticData.username);
			break;
		case ACTION_DISPLAY_ALL_EXAMS:
			l.showContextMenuForChild(v);
			break;
		case ACTION_LOGOUT:
			finish();
			break;
		}
	}
	
	@Override
	public boolean onContextItemSelected(android.view.MenuItem item) {
		mProgressDialog = ProgressDialog.show(MenuActivity.this,    
				getString(R.string.loading_please_wait), 
				getString(R.string.loading_verifying_login), true);
		Api.enrollmentExamDatesRequest(mListener, ""+item.getItemId());
		return true;
	}

	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
			ContextMenuInfo menuInfo) {
		super.onCreateContextMenu(menu, v, menuInfo);
		menu.setHeaderTitle(R.string.exams_contextTitle);
		for(Integer k: mEnrollments.keySet()) {
			menu.add(Menu.NONE, k, Menu.NONE, mEnrollments.get(k));
		}
	}

	public void onServerResponse(Object o) {
		mProgressDialog.dismiss();
		if (o != null && o instanceof StudentEnrollments) {
			StudentEnrollments le = (StudentEnrollments)o;
			mEnrollments.clear();
			for(Iterator<StudentEnrollment> i = le.enrollments.iterator(); i.hasNext(); ) {
				StudentEnrollment e = i.next();
				mEnrollments.put(e.key, e.study_program + "(" + e.study_year + ")");
			}
			getListView().showContextMenu();
		} else if (o != null && o instanceof EnrollmentExamDates) {
			EnrollmentExamDates le = (EnrollmentExamDates)o;
			StaticData.mEnrollmentExamDates.clear();
			for(Iterator<EnrollmentExamDate> i = le.EnrollmentExamDates.iterator(); i.hasNext(); ) {
				EnrollmentExamDate e = i.next();
				StaticData.mEnrollmentExamDates.put(e.exam_key, e);
			}
			Intent intent = new Intent(this, ExamsActivity.class);
			startActivity(intent);
		} else {
			Toast.makeText(this, getString(R.string.communication_error), 2000).show();
		}
	}
}