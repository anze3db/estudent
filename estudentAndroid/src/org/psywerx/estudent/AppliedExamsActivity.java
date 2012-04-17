package org.psywerx.estudent;

import java.util.ArrayList;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class AppliedExamsActivity extends ListActivity {

	private ProgressDialog m_ProgressDialog = null;
	private ArrayList<MenuItem> m_orders = null;
	private OrderAdapter m_adapter;
	private Runnable viewOrders;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.menu_layout);
		m_orders = new ArrayList<MenuItem>();
		this.m_adapter = new OrderAdapter(this, R.layout.row, m_orders);
		setListAdapter(this.m_adapter);

		viewOrders = new Runnable(){
			public void run() {
				getExamsList();
			}
		};
		Thread thread =  new Thread(null, viewOrders, "MagentoBackground");
		thread.start();
		m_ProgressDialog = ProgressDialog.show(AppliedExamsActivity.this,    
				"Please wait...", "Retrieving data ...", true);
	}
	private Runnable returnRes = new Runnable() {
		public void run() {
			if(m_orders != null && m_orders.size() > 0){
				m_adapter.notifyDataSetChanged();
				for(int i=0;i<m_orders.size();i++)
					m_adapter.add(m_orders.get(i));
			}
			m_ProgressDialog.dismiss();
			m_adapter.notifyDataSetChanged();
		}
	};
	private void getExamsList(){		
		try{
			m_orders = new ArrayList<MenuItem>();
			MenuItem o1 = new MenuItem();
			o1.setItemName("SF services");
			o1.setItemDescription("Pending");
			MenuItem o2 = new MenuItem();
			o2.setItemName("SF Advertisement");
			o2.setItemDescription("Completed");
			m_orders.add(o1);
			m_orders.add(o2);
			Thread.sleep(1500);
			Log.i("ARRAY", ""+ m_orders.size());
		} catch (Exception e) {
			Log.e("BACKGROUND_PROC", e.getMessage());
		}
		runOnUiThread(returnRes);
	}
	private class OrderAdapter extends ArrayAdapter<MenuItem> {

		private ArrayList<MenuItem> items;

		public OrderAdapter(Context context, int textViewResourceId, ArrayList<MenuItem> items) {
			super(context, textViewResourceId, items);
			this.items = items;
		}
		@Override
		public View getView(int position, View convertView, ViewGroup parent) {
			View v = convertView;
			if (v == null) {
				LayoutInflater vi = (LayoutInflater)getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				v = vi.inflate(R.layout.row, null);
			}
			MenuItem o = items.get(position);
			if (o != null) {
				TextView tt = (TextView) v.findViewById(R.id.toptext);
				TextView bt = (TextView) v.findViewById(R.id.bottomtext);
				if (tt != null) {
					tt.setText("Name: "+o.getItemName());                            }
				if(bt != null){
					bt.setText("Status: "+ o.getItemDescription());
				}
			}
			return v;
		}
	}
}