package com.swp.ontop.ui.functions

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.swp.ontop.R
import com.swp.ontop.databinding.FragmentFunctionsBinding

class FunctionsFragment : Fragment() {

    private lateinit var functionsViewModel: NotificationsViewModel
    private var _binding: FragmentFunctionsBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        functionsViewModel =
            ViewModelProvider(this).get(NotificationsViewModel::class.java)

        _binding = FragmentFunctionsBinding.inflate(inflater, container, false)
        val root: View = binding.root
        val cont = activity?.applicationContext
        val toast = Toast.makeText(cont, "Wasser kommt", Toast.LENGTH_LONG)
        val pump = binding.pump;
        pump.setOnClickListener {
            // Instantiate the RequestQueue.
            val queue = Volley.newRequestQueue(cont)
            val url = "http://ontop.hs-bochum.de/control/activatePumpMain.php"

            val stringRequest = StringRequest(
                Request.Method.GET, url,
                Response.Listener<String> { response ->
                    toast.setText("Wasser kommt")
                },
                Response.ErrorListener { toast.setText("Leider gibt es Verbindungsprobleme!" )})

            queue.add(stringRequest)
            toast.show()
        }
        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}