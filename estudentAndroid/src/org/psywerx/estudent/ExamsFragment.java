package org.psywerx.estudent;

import java.util.ArrayList;
import java.util.List;

import org.psywerx.estudent.extra.HelperFunctions;
import org.psywerx.estudent.json.EnrollmentExamDates.EnrollmentExamDate;

import android.app.Activity;
import android.app.ListFragment;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;

public class ExamsFragment extends ListFragment {
	
	private Context mContext;
	
	private MenuAdapter mMenuAdapter;
	private OnExamSelectedListener mExamSelectedListener;
	
	public interface OnExamSelectedListener {
		public void onExamSelected(int action);
	}
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mContext = getActivity().getApplicationContext();
		
		List<MenuItem> menu = new ArrayList<MenuItem>();
		
		for(Integer k: StaticData.mEnrollmentExamDates.keySet()) {
			EnrollmentExamDate e = StaticData.mEnrollmentExamDates.get(k);
			menu.add(new MenuItem(e.course + " (" + e.exam_key + ")", HelperFunctions.dateToSlo(e.date), e.exam_key, R.drawable.check_ok_128));
			//if prijavlen else menu.add(new MenuItem(e.course, "("+e.exam_key+")", e.exam_key));
		}

		mMenuAdapter = new MenuAdapter(mContext, menu);
		setListAdapter(mMenuAdapter);
	}
	
	@Override
	public void onAttach(Activity activity) {
		super.onAttach(activity);
		mExamSelectedListener = (OnExamSelectedListener) activity;
	}
	
	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
		super.onListItemClick(l, v, position, id);
		
		mExamSelectedListener.onExamSelected(mMenuAdapter.getItem(position).getAction());
	}

}
