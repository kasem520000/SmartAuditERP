# التحقق وخطط القبول —7B27/R4k

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ الفرع `arena/94ae8414-smartauditerp`. دخول B27 بعد تسليم B26 المدفوع `6eedc0640e3432c14ca0875b7f1c7806ea1e3f64`،770 مادة و 326 نتيجة. ساعة تجميد الدخول المرصودة `2026-11-20T01:15:07.156974+00:00` حقل مستقل؛ لا تعيد تأريخ المرجع أو أي capture سابق.

**ساكن فقط، دون إصلاح أو تشغيل ERP. R4k شريحة محدودة؛7B/7 جزئيتان؛R4l/7B28 مقترح أو split مسبب؛7C لم تبدأ؛8 غير مأذونة هنا.** الإصلاح في محادثة وفرع مستقلين؛ لا نفترض بدءه أو تزامنه، ولا نؤلف ملفات إصلاح أو ندمج repair→audit أو نغلق نتائج. `next_phase=8` تخطيط متابعة لا تفويض.

[النتائج](PHASE-07B27.md) · [العقود](INVOICE-SEARCH-CONTRACTS-07B27.md) · [التحقق والخطط](VALIDATION-07B27.md) · [المتبقي](PHASE-07-REMAINING-07B27.md) · [هوية التاريخ والالتقاط](DATE-IDENTITY-NOTE-07B27.md) · [النطاق](review-scope-07B27.csv) · [قرار النطاق](evidence/scope-decision-07B27.json) · [السجل](findings.csv) · [stdout الرسمي](evidence/checks-07B27.json)

## 1. ما نُفذ وما لم ينفذ

- فحص دخول حقيقي مستقل عند 6eedc06:326 نتيجة/827 أصلاً/786 حالة وثائقية/27 مجموعة/errors[]/exit0/stderr فارغ. لم يستبدل stdoutB26 الرسمي.
- اجتازت كل 48 حالة B26 الأصلية طفل OWN326/raw327CRLF/indexes/presetB26 و A محلياً للمجموعة؛ لم يحرر أي ملف محمي. B25/44 و B24/44 منفصلتان محفوظتان.
- اجتاز فحص B27 عبر **CLI الافتراضي الفعلي 838 حالة وثائقية في 28 مجموعة** =786 محفوظة +52 جديدة؛329 نتيجة و 827 أصلاً مطابقاً و errors[] و exit0 و stderr فارغ. ليست 838 اختبار ERP أو تنفيذ 36 خطة قبول؛ تبقى خطط التطبيق متكاملة not-executed.
- نُفذت **32 وضعية تاريخية OWN فعلياً**:2–6 و A و B1–26، كلها exit0/errors[]/827/stderr فارغ. [أرشيف التنفيذ](evidence/historical-mode-verification-07B27.json) حجمه 95343 بايت،SHA-256:`39c0706f8b13a61a9385f0c9595889141f67846e88b48c43b9116ab58dbd5392`؛ يحفظ نتائج العمليات وهويات stdout وبصمات الأدوات **عند الالتقاط**. ليس synthetic32 fixture أو إعادة إنتاج للأرشيف الأصلي، ولا ادعاء إعادة 32 بأدوات نهائية بعد تثبيت بصمة الأرشيف والنثر والفهارس والدفع.

- الشاهد الناجح الفعلي 46921 بايت/20 مثالاً خاملاً/20 مطابقة نصية/errors[]/exit0/stderr فارغ، وله محاولة جديدة فاشلة سابقة محفوظة، لا ERP failure.
- **كل 36 خطة قبول متكاملة not-executed**؛ كذلك 32 خطة B26 السابقة لم تنفذ. نجاح صيانة وثائق متداخلة لا يورد عقود الخطة الخارجية أو ينفذ كل إجرائها أو يقبل التطبيق.

| المادة | bytes / SHA-256 | حد الهوية |
| --- | --- | --- |
| findings-through-07B26.csv | 217156 / `0ea4b60648757a98bd602049f22cb82900d0c1d28a2f7674a9e47e04c50ccb81` | 326/raw327CRLF/noBOM؛ الحالي 329 يبدأ ببايتاتها بالضبط. |
| shared-indexes-through-07B26.json | 298406 / `eed5196df7fb8315640e70ae130bb3d2f6afd56cf49e4829d788573bf8eb2d27` | ثلاثة نصوص دخول B26 دقيقة؛ ليست الفهارس الحالية. |
| provenance-07B27.json | 87056 / `4d409375f70407e6f0844bc891a3488a868e663cb9a25ae4767451299edac61d` | 765 مادة محمية من 770، وثلاثة freezes لا تعاد. |
| invoice-search-witnesses-07B27.json | 46921 / `bd7ac7a05efd39e44263ef155fcd216555d272c534fe7b098e75e5bbde1d4dd1` | التقاط ناجح مستقل،لا SQL/DataView/WPF/SDK أو saved loss. |
| invoice-search-witness-attempt-01-07B27.json | 46941 / `bc1a4e4f62d634fe6154af71405063b54976b92f8530bb7583033462194b0009` | التقاط فاشل محفوظ،exit1/errors[ST7B27-19]؛ لا يحتسب ناجحاً. |
| historical-mode-verification-07B27.json | 95343 / `39c0706f8b13a61a9385f0c9595889141f67846e88b48c43b9116ab58dbd5392` | ملخص نتائج 32 subprocess وهويات stdout وأدوات وقت الالتقاط، لا النص الكامل للتيارات. |
| checks-07B26.json | 228846 / `f80ef7936aca23c3667d44c48821a66dc1704203598ce1ea0bd9ed687edd5895` | 228846 بايت/capturedd38f97،لا delivery-entry6eedc06؛ ثابت لا يعاد بعد الدفع. |

stdoutB27 الرسمي يلتقط حصرياً مباشرة من CLI الافتراضي الفعلي بعد اكتمال المواد، لا JSON مركباً من المجاميع أو placeholder. فحص ما بعد الدفع مستقل في مساحة مؤقتة، ولا يستبدل الملف الرسمي أو الأرشيف. API main defaultB15 باقٍ.

## 2. سجل 32 وضعية تاريخية حقيقية

كل صف أدناه من subprocess فعلي؛exit0/errors[]/827/stderr0/ERP0. علامة— تعني aggregate غير مبلغ عنه، لا 0. الأرشيف يحفظ commands و bytes/SHA/exit/registry/cases/suites وبصمات الأدوات عند الالتقاط؛ الخام في مساحة التحقق المؤقتة، وليس ضمن Git أو الأرشيف. لا نستبدل تياراً مفقوداً ببيانات مصطنعة.

| الوضعية | عدد OWN | cases / suites المبلغ عنها | registry_used |
| --- | --- | --- | --- |
| phase2 | 49 | — / — | `evidence/findings-through-02.csv` |
| phase3 | 74 | — / — | `evidence/findings-through-03.csv` |
| phase4 | 106 | — / — | `evidence/findings-through-04.csv` |
| phase5 | 137 | — / — | `evidence/findings-through-05.csv` |
| phase6 | 172 | — / — | `evidence/findings-through-06.csv` |
| A | 200 | — / — | `evidence/findings-through-07A.csv` |
| B1 | 223 | — / — | `evidence/findings-through-07B1.csv` |
| B2 | 237 | 44 / 3 | `evidence/findings-through-07B2.csv` |
| B3 | 248 | 62 / 4 | `evidence/findings-through-07B3.csv` |
| B4 | 261 | 82 / 5 | `evidence/findings-through-07B4.csv` |
| B5 | 266 | 104 / 6 | `evidence/findings-through-07B5.csv` |
| B6 | 270 | 132 / 7 | `evidence/findings-through-07B6.csv` |
| B7 | 276 | 156 / 8 | `evidence/findings-through-07B7.csv` |
| B8 | 280 | 184 / 9 | `evidence/findings-through-07B8.csv` |
| B9 | 282 | 208 / 10 | `evidence/findings-through-07B9.csv` |
| B10 | 285 | 236 / 11 | `evidence/findings-through-07B10.csv` |
| B11 | 287 | 266 / 12 | `evidence/findings-through-07B11.csv` |
| B12 | 289 | 298 / 13 | `evidence/findings-through-07B12.csv` |
| B13 | 291 | 322 / 14 | `evidence/findings-through-07B13.csv` |
| B14 | 294 | 350 / 15 | `evidence/findings-through-07B14.csv` |
| B15 | 298 | 382 / 16 | `evidence/findings-through-07B15.csv` |
| B16 | 299 | 410 / 17 | `evidence/findings-through-07B16.csv` |
| B17 | 300 | 434 / 18 | `evidence/findings-through-07B17.csv` |
| B18 | 302 | 462 / 19 | `evidence/findings-through-07B18.csv` |
| B19 | 307 | 498 / 20 | `evidence/findings-through-07B19.csv` |
| B20 | 310 | 530 / 21 | `evidence/findings-through-07B20.csv` |
| B21 | 313 | 566 / 22 | `evidence/findings-through-07B21.csv` |
| B22 | 316 | 606 / 23 | `evidence/findings-through-07B22.csv` |
| B23 | 319 | 650 / 24 | `evidence/findings-through-07B23.csv` |
| B24 | 322 | 694 / 25 | `evidence/findings-through-07B24.csv` |
| B25 | 324 | 738 / 26 | `evidence/findings-through-07B25.csv` |
| B26 | 326 | 786 / 27 | `evidence/findings-through-07B26.csv` |

الحالة 20 في المجموعة الجديدة تستعمل synthetic32 لاختبار رفض schema، **لا إثبات تنفيذ 32**؛ الحالة 21 تتحقق من الأرشيف الحقيقي ببصمة مستقلة. B26 لا يستخدم live329 أو defaultB27 لتأكيداته التاريخية؛[الطفل الصريح](tools/run_historical_bulk_product_tests_07B27.py) يختار presetB26 ومدخلات OWN326/raw327CRLF/indexes و A محلياً ثم يعيد A/preset في finally. لا حالة محذوفة أو متخطاة أو مرشحة، ولا global Path/shared subprocess patch أو disk overlay/rebaseline. فحص CLI الحالي B27 و versionedB26 و API15 مستقل.

بعد التقاط 32 تغير ملف checker جديد واحد فقط: helperB27 لتثبيت SHA الأرشيف الفعلي. بقيت الاختبارات الجديدة 52 وأدوات الالتقاط الأخرى كما كانت. أثبتت حراسة التسليم تطابق نسخة helper وقت الالتقاط مع إعادة بنائها من النسخة النهائية بعكس سطر pin في الذاكرة ومقارنة SHA، دون كتابة overlay أو تعديل الأرشيف. الفحص المجمع 838/28 أُجري بعد ذلك؛ لا ينسب إلى 32 ادعاء إعادة شاملة بالأدوات النهائية أو بعد الدفع.

### المحاولة الجديدة الفاشلة ليست عيب تطبيق

أخفقت ST7B27-19 في الالتقاط الأول لأن نطاق النص لم يشمل IsChecked=True. بقي 46941 بايت/exit1/errors[ST7B27-19] محفوظاً دون تعديل. صحح نطاق الملاحظة داخل XAML1–561 المعلن كاملاً أصلاً إلى 238–270، وصحح مجال زر المسح إلى 345–353 ودليل combo إلى 229–235؛ لا توسعة scope أو تعديل مصدر تطبيق أو tool محمي. أُنشئ stdout ناجح آخر حصري 46921 بايت/exit0/errors[]/stderr0. لا يعني ذلك أن شاشةERP شغلت أو فشلت أو أصلحت. أسبقية التصحيحات بين preflight والمحاولة الرسمية موضحة بحدودها؛ لا تزعم أن كلها حدث بعد المحاولة نفسها.

أعيد تحقق baseline بقراءة فقط:827 مساراً و 29,128,444 بايت مطابقة، و xml_parse_errors=0 و xaml_name_mismatches=0 و dotnet_available=false؛exit0 و stderr فارغ. لم يستعمل--write أو ينفذ بناء.NET.

## 3. 20 مثالاً خاملاً و 20 ملاحظة نصية

[collector](tools/check_invoice_search_witnesses.py) يستعمل stdlib فقط، دون استيراد التطبيق أو SDK أو تشغيل SQL/DataView/WPF. يقرأ بايتات كاملة للبصمة وفهرسة الأسطر؛ العمق الدلالي هو المجالات 11 المعلنة فقط،وملفا البحث كاملان محلياً دون تعميم على المحيط. السجلات اصطناعية بـGlobalID مميز وأعداد صغيرة وأيام ترتيبية، لا calendars أو ثقافة أو معنى حالة تجارية.

| الشاهد | الأصل والملاحظة | الحد |
| --- | --- | --- |
| ALG7B27-01 | P7-155<br>Changing selected process2 to1 cannot recover source rows | Explicit successful supplied query and handler call, not WPF event order or a real empty database. |
| ALG7B27-02 | P7-155<br>All selection still contains only server process2 | The All option cannot broaden the already restricted snapshot; no UI/SQL run. |
| ALG7B27-03 | P7-155<br>Selecting the original process2 is a positive control | Agreement for the original criterion does not validate switching criteria. |
| ALG7B27-04 | P7-155<br>Fresh server process1 has the records absent from old snapshot | Counterfactual predicate control, not an application fix or executed reload. |
| ALG7B27-05 | P7-156<br>Initial caller eligibility excludes status0 | Status meanings remain external; the caller explicitly requires the literal value1. |
| ALG7B27-06 | P7-156<br>from-date replaces rather than combines caller predicate | Same156 root for both date handlers; ordinal-day fixture, not DateTime/culture/provider semantics. |
| ALG7B27-07 | P7-156<br>to-date replaces rather than combines caller predicate | Same156 root for both date handlers; ordinal-day fixture, not DateTime/culture/provider semantics. |
| ALG7B27-08 | P7-156<br>Clear removes the caller condition and reloads | Reset of optional fields is not authorization to remove mandatory eligibility. |
| ALG7B27-09 | P7-156<br>Branch and deletion remain guarded after Cond replacement | Positive local guards, not a deployed ACL, schema or concurrency acceptance claim. |
| ALG7B27-10 | P7-156<br>The new date condition actually filters a distinct day | Only a bounded predicate contrast, not an end-of-day/timezone/.NET parser oracle. |
| ALG7B27-11 | P7-157<br>A purchase type1 request also admits type20 | Supplied distinct GlobalIDs and successful source rows; no deployed access or saved mutation observed. |
| ALG7B27-12 | P7-157<br>Selection retains GlobalID but does not carry an allowed type | Not061 local-number identity loss; no requirement inferred for every DTO or all callers. |
| ALG7B27-13 | P7-157<br>Purchase consumer GID+branch lookup maps the type20 source | Only the selected reader/type boundary, not a completed Navigate render, invoice save or loss. |
| ALG7B27-14 | P7-157<br>Requested type1 record remains a positive control | Ordinary success does not justify unconditional type20 for purchase/transfer. |
| ALG7B27-15 | P7-157<br>Special type23 branch is exact and does not append20 | The separate InvContratct table is a text contrast, not its schema acceptance. |
| ALG7B27-16 | P7-157<br>Default not-done result is not consumed | No all-modal-path certification, actual Close/Hide behavior not executed. |
| ALG7B27-17 | P7-157<br>Consumer branch mismatch is a positive nonmatch control | Does not prove deployed authorization or type/eligibility revalidation. |
| ALG7B27-18 | P7-157<br>Equal local numbers do not confuse the retained GlobalID lookup | A narrowing control distinguishing this cause from061; uniqueness is supplied, not measured. |
| ALG7B27-19 | P7-156<br>Receive caller consumes selected GID without restoring status predicate | No assertion of actual stock receipt or final save; literal caller constraint alone is established. |
| ALG7B27-20 | P7-157<br>Request20 matches its record once despite OR20 | Logical OR is not UNION duplication; type20 may be intentional in specifically authorized caller contracts. |

كل ST7B27-01…20 تطابق نصياًحقول الطلب والباني والمرشحات والاختيار والقارئ وضوابط الفترة والفرع والحذف؛كل documented_text_observation_matches=true و source_application_executed=false. صحة النصلا تصادقعلى event ordering أو parse أو تكامل المخطط أو حالة القاعدة أو حفظ الخسارة.

## 4. 52 حالة وثائقية جديدة — كل 786 السابقة محفوظة

| الحالة | العقد الذي تحرسه |
| --- | --- |
| 01 | `test_01_OWN326_exact_raw327CRLF_three_texts` |
| 02 | `test_02_reject_bad_OWN_rows_bytes_BOM_LF_texts` |
| 03 | `test_03_context_local_Path_not_global_or_disk_overlay` |
| 04 | `test_04_nested_OWN324_and_exception_restoration` |
| 05 | `test_05_frozen_rows_texts_copy_isolation` |
| 06 | `test_06_all326_fields_ALLnextphase_evidence_rawprefix` |
| 07 | `test_07_only155_156_157_append_raw330CRLF_noBOM` |
| 08 | `test_08_exact_G223_append224through228_only` |
| 09 | `test_09_sentinels_expand_before_dedup_RC_regression` |
| 10 | `test_10_ordered_SC8_DS8_proc_eligibility_type_GID_limits` |
| 11 | `test_11_ledger_responsibilities_nonempty_not_executed` |
| 12 | `test_12_FE18_INV18_T36_reverse_links_three_specific_roots` |
| 13 | `test_13_distinct_invariants_criteria_and_responsibilities` |
| 14 | `test_14_all14_residual_ancestry_hash_contracts` |
| 15 | `test_15_full_old_inputs_all_routes_and_no_approval` |
| 16 | `test_16_three_split_ancestries_full_inputs_and_reasons` |
| 17 | `test_17_boundedR4k_fourB_sixC_unstarted_no_percent_or_sessions` |
| 18 | `test_18_witness_strict_boolean_integer_limits_B10_addendum` |
| 19 | `test_19_actual_successful_witness_hash_readonly_recompute` |
| 20 | `test_20_synthetic32_schema_OWN326_ALL48_not_execution_evidence` |
| 21 | `test_21_actual32_archive_hash_identity_separate_from_schema_fixture` |
| 22 | `test_22_server2_selected1_empty_All_remains_only2` |
| 23 | `test_23_same2_and_fresh1_controls_not_executed_reload` |
| 24 | `test_24_both_explicit_date_actions_drop_status1_same_root156` |
| 25 | `test_25_clear_drops_mandatory_eligibility_no_WPF_event_count` |
| 26 | `test_26_date_really_filters_branch_deleted_positive_controls` |
| 27 | `test_27_receive_consumer_does_not_restore_status1_not_stock_save` |
| 28 | `test_28_purchase1_source_includes20_not_requested1_only` |
| 29 | `test_29_projection_retains_GID_not061_omits_allowed_type` |
| 30 | `test_30_selected_GID_consumer_maps_actual20_type1_control` |
| 31 | `test_31_special23_exact_and_request20_no_OR_duplication` |
| 32 | `test_32_not_done_sentinel_and_branch_mismatch_not_consumed` |
| 33 | `test_33_equal_local7_uses_GID_positive_control_not_uniqueness_proof` |
| 34 | `test_34_supplied_records_strict_shape_unique_nonsecret_ids_types` |
| 35 | `test_35_explicit_actions_condition_domain_not_arbitrary_SQL` |
| 36 | `test_36_integer_and_ordinal_fixture_bounds_not_calendar_parser` |
| 37 | `test_37_selection_consumer_explicit_shape_no_DTO_defaults` |
| 38 | `test_38_ACTUAL_B27_parser_versioned_B26_B25_B24_API15` |
| 39 | `test_39_actual_entrypoint_OWN26_before_current27` |
| 40 | `test_40_exact_argv_proxy_preserves_unrelated_calls_kwargs` |
| 41 | `test_41_view_exception_restore_no_global_Path_or_shared_subprocess_patch` |
| 42 | `test_42_historical_child_ALL48_local_A_and_protected26_25_24_tools` |
| 43 | `test_43_actual326_exact_fields_barriers_three_entry_freezes` |
| 44 | `test_44_scope7_overlap6_new1_union426_actual11reads_two_whole` |
| 45 | `test_45_only_three_adjudicated_roots_prior_nearest_not_recounted` |
| 46 | `test_46_actual14_residuals_three_splits_full_inputs_routes_currentlinks` |
| 47 | `test_47_reference_clock_source_capture_delivery_identities_separate` |
| 48 | `test_48_collector_stdlib_only_no_app_execution_and_protected765` |
| 49 | `test_49_failed_new_attempt_retained_exact_not_counted_passed` |
| 50 | `test_50_all20illustrations20lexical_pass_inert_explicit_limits` |
| 51 | `test_51_documentref_followup_not_existing_contract_and_evidence_in_scope` |
| 52 | `test_52_every_capability_has_substantive_responsibility_two_unexecutedplans` |

لا تعديل للاختبارات التاريخية أوتصفية أوتخط لإمرار الحاضر. OWN هو مدخل خاص بكل cutoff، لا حقيقة مركبة من  registry حالي. كل 52 الجديدة تؤكد حدود fixtures ومسؤوليات وخطط وهويات وثائق، لا 52 تجربةأعمال.

## 5. 36 خطة قبول متكاملة — كلها not-executed

لكل صف prerequisites و owner_role و safety_controls ودليل وسببفي[CSV الكامل](evidence/acceptance-tests-07B27.csv). الإذن والبيئة المستقلان والعقود المنقحة تسبق أي تنفيذ؛ تستخدم مدخلات اصطناعية وعزلاً يحمي الأعمال والأسرار. أدناه الإجراء ومعياره، لا أوامر تنفذها أدوات التدقيق. وجود فحص وثائقي حالي يشترك مع جزء من الخطة لا ينفذها بكاملها.

| الخطة والقدرة والأصل | السيناريو والإجراء المقترح | معيار القبول غير المنفذ |
| --- | --- | --- |
| P7B27T-01<br>FE7B27-01 / P7-155 | التحويل 2 إلى 1<br>بعد إذن مستقل جهز نقلتين من النوع 8 بعمليتين 1 و 2 في فرع واحد؛ افتح search2 ثم اختر 1 وتتبع query/snapshot/view. | يصل صف العملية 1 الصحيح إلى اللقطة والعرض أو يعلن أن الاختيار غير مدعوم؛لا empty كاذبة من استبعاد سابق.<br>**not-executed** |
| P7B27T-02<br>FE7B27-01 / P7-155 | All وضابط نفس 2<br>قارن All0 ونفس 2 على اللقطة ثم إعادة تحميل معيار 1 مستقلة بعقد دعم منقح. | All يعكس مجموعة العمليات المصرح بها، ونفس 2 لا يبرر حجب 1؛ النتيجة تحفظ معاييرها الفعلية.<br>**not-executed** |
| P7B27T-03<br>FE7B27-02 / P7-156 | تغيير التاريخ يحذف الأهلية<br>ورد صفين 8/1 في فرع واحد وتاريخ واحد،status1 و status0؛بعد caller-status1 استدع from-date ثم to-date منفصلين وقارن ما يصل للعرض والمستهلك. | يبقى status0 خارج allowed result في كلتا الحالتين؛التاريخ يضاف إلى قيد caller ولا يستبدله.<br>**not-executed** |
| P7B27T-04<br>FE7B27-02 / P7-156 | تصفية الحقول تحفظ شرط المتصل<br>من نفس المدخل فعّل clear ثم اختر صفاً واقرأ request/selection/consumer دون كتابة؛أضف branch/deleted controls. | reset يزيل المرشحات الاختيارية فقط،وتعاد أهلية status1 عند الاختيار والاستهلاك بلا أثر مخزون مدعى.<br>**not-executed** |
| P7B27T-05<br>FE7B27-03 / P7-157 | نوع 20 يدخل طلب 1<br>ورد فاتورتين مستقلتين GlobalID بنوع 1 و 20 وعملية 1 وفرع واحد؛قارن مصدر search ونوع النتيجة وخريطة BindingInvoice. | تستبعد 20 من طلب مشتريات 1 أو يسمح بها عقد صريح ومتصل متوافق؛لا تحميل نوع غير مقصود بصمت.<br>**not-executed** |
| P7B27T-06<br>FE7B27-03 / P7-157 | نوع 1 و 23 وضوابط الهوية<br>قارن type1 السليم و special23 و request20 ونفس الرقم المحلي لصفين مختلفين؛افصل GID عن النوع. | GlobalID يحدد الصف الصحيح ولا يستخدم كبديل لقبول نوعه؛23 لا يضم 20،و OR20 ليس تكرار UNION.<br>**not-executed** |
| P7B27T-07<br>FE7B27-04 / P7-155 | ربط الزر والمدخل<br>في بيئة مستقلة مأذونة تتبع click من XAML إلى constructor2/8 ثم تأكد أن مصدر options يعود للطلب نفسه. | يثبت origin2/8 في الطلب ولا تقاس تغطية كل المتصلين من هذا الزر.<br>**not-executed** |
| P7B27T-08<br>FE7B27-04 / P7-155 | عقد صلاحيات التحكم<br>ورد permission/settings manifest منقح يبين إن كان selector يعطل خارجياً،وقارن فتحه المتاح بمحلياته. | الحكم يقيد بالمسار المدعوم ولا يفترض إعدادات خارجية أو bypass نشر.<br>**not-executed** |
| P7B27T-09<br>FE7B27-05 / P7-156 | الحالة المسموحة<br>قدم قاموس status وأمر receive منقحاً ثم قارن status1 و 0 مع مصدرين وفرعين. | لكل حالة أهلية مقصودة موثقة أو رفض صريح بلا إعادة تفسير رقم 1.<br>**not-executed** |
| P7B27T-10<br>FE7B27-05 / P7-156 | ثبات شرط العملية<br>غير optional date/name فقط مع combo معطل كما في المتصل؛تتبع مصدر الأهلية مستقلاً. | تعطيل combo لا يحفظ InvoiceStatus تلقائياً،ويظل شرط caller مستقلاً.<br>**not-executed** |
| P7B27T-11<br>FE7B27-06 / P7-156 | from-date منفرد<br>ورد قيد status1 ثم حدين اصطناعيين صحيحين واستدع from-date وحده بعد التمكين. | الطلب الناتج يضم الأهلية والتاريخ معاً ولا يتسع إلى status0.<br>**not-executed** |
| P7B27T-12<br>FE7B27-06 / P7-156 | to-date منفرد وفشل<br>كرر to-date وحده،ثم فشل provider مفترض في مضاعف بعد الإذن؛افصل healthy عن stale. | تبقى الأهلية ومصدر snapshot معلومين،ولا تتحول النتيجة القديمة إلى نجاح تحت طلب جديد.<br>**not-executed** |
| P7B27T-13<br>FE7B27-07 / P7-156 | clear من status1<br>جهز request بأهلية إلزامية ومرشحات اسم/تاريخ اختيارية؛استدع clear وتحقق من source plan قبل العرض. | تمحى الاختيارات الثانوية فقط ولا يضيع status1 أو مصدر allowed-set.<br>**not-executed** |
| P7B27T-14<br>FE7B27-07 / P7-156 | cancel/فشل reset<br>بعد عقد outcome مستقل افحص إلغاء النافذة وفشل reload أثناء reset في مضاعف معزول. | الإلغاء والفشل لا يعيدان selected قديمة تحت طلب أوسع ولا يقران حفظاً.<br>**not-executed** |
| P7B27T-15<br>FE7B27-08 / P7-155 | العمليات الغائبة<br>ولد لقطة process2 فقط وفلاتر 0/1/2 ونفس بيانات source الكاملة في مضاعف وثائقي مستقل. | تعرف القيود السابقة في snapshot وتحدد الحاجة للتحميل عند توسيع المعايير.<br>**not-executed** |
| P7B27T-16<br>FE7B27-08 / P7-155 | الصحة والنصوص<br>ورد عقد literal/contains وال culture ثم افحص الاقتباس والفشل بخطة منفصلة عن نموذج int. | لا ينسب نجاح predicate صحيح إلى قبول DataView لكل نص؛074-family لا تعاد عدها.<br>**not-executed** |
| P7B27T-17<br>FE7B27-09 / P7-157 | نوع 23 مقابل 1<br>جهز source tables وهمية مستقلة بعقد مفصح؛قارن طلب 23 exact مع 1 و 8 و 20. | التحويل إلى مصدر آخر معلن وتنفذ مجموعةأنواع مقصودة لااستثناء 20 لكل طلب.<br>**not-executed** |
| P7B27T-18<br>FE7B27-09 / P7-157 | الفرع والمحذوف<br>قارن فرعاً آخر ومحذوفاً في الطلبات المحلية مع حالة 14 التي تستثني branch نصياً. | يحفظ ضابطا branch/deleted حيث ينصان؛14 تحتاج عقد caller لا اعتماد كل الفروع أو ACL.<br>**not-executed** |
| P7B27T-19<br>FE7B27-10 / P7-157 | هوية محفوظة ونوع غير منقول<br>قارن صف مصدر من النوع 20 بصف العرض ثم بنتيجة الاختيار، ووثق الحقول التي عبرت الحد والحقول التي لم تعبره. | يفصل عقد الهوية عن عقد السماح بالنوع؛ لا تخترع حقول أو defaults في DTO.<br>**not-executed** |
| P7B27T-20<br>FE7B27-10 / P7-157 | رقم محلي متساو و GlobalID مختلف<br>ورد صفين برقم محلي 7 وهويتي GlobalID مختلفتين، أحدهما نوع 1 والآخر 20؛ تتبع الاختيار المعتمد على GlobalID. | يحافظ GlobalID على الصف المحدد، لكن صحة المفتاح وحدها لا تسمح بنوع خارج مجموعة الطلب.<br>**not-executed** |
| P7B27T-21<br>FE7B27-11 / P7-156;P7-157 | الاختيار العادي<br>بعد إذن مستقل قارن حمولة Enter والنقر المزدوج لصف معلوم مع سياق الاستعلام نفسه، دون حفظ. | لا تنفصل نتيجة Accepted عن قيود الطلب النوعية والإلزامية، بصرف النظر عن gesture الاختيار.<br>**not-executed** |
| P7B27T-22<br>FE7B27-11 / P7-156;P7-157 | زر الإرجاع والإلغاء<br>ورد عقد زر الإرجاع مقابل الاختيار العادي، ثم قارن الإلغاء بلا اختيار بالممر الخاص في خطة مستقلة. | لكل مسار معنى معلوم؛ لا يفترض أن فحص IsPreviousReturned حارس عام، ولا يعد تجاوزه جذراً جديداً هنا.<br>**not-executed** |
| P7B27T-23<br>FE7B27-12 / P7-157 | طلب مشتريات من النوع 1<br>ثبت طلب 1/1 وفرع 1 ثم أعد صف 20 من مضاعف بحث معزول بعد إذن مستقل. | يرفض النوع الخارج عن المسموح قبل تسليم الاستعلام إلى القارئ، أو يعلن دعمه بعقد صريح ومتصل متوافق.<br>**not-executed** |
| P7B27T-24<br>FE7B27-12 / P7-157 | الإلغاء والهوية الحارسة<br>قارن ISDone=false و GlobalID=-1 بنتيجة نوع 1 صحيحة في المستهلك. | الإلغاء لا يستدعي البحث اللاحق، والنجاح لا يخلط صلاحية الهوية بالسماح بالنوع.<br>**not-executed** |
| P7B27T-25<br>FE7B27-13 / P7-156 | صف status0 بعد المسح<br>أعد صفاً غير مطابق للقيد الحرفي status1، كما يسمح الاستعلام بعد المسح؛ تتبع شرط الأهلية قبل القارئ. | يعيد المستهلك التحقق من قيد status1 المقصود، ولا يعتمد على إخفاء الصف في لقطة سابقة.<br>**not-executed** |
| P7B27T-26<br>FE7B27-13 / P7-156 | حاجز التنفيذ والتزامن<br>ورد عقد الأهلية عند التنفيذ والمخطط والإصدار، ثم أعد خطة فشل وإعادة محاولة بعد إذن مستقل. | نجاح البحث ليس قبولاً ذرياً، ولا يحسم P4-019 أو المخاطر 014/020/021.<br>**not-executed** |
| P7B27T-27<br>FE7B27-14 / H7B27-05 | سجل الاحتمالات المتبقية<br>اعزل كل احتمال بمعيار واستبعاد ومالك ومدخل، واقترح نطاقاً تالياً قبل إثبات نتيجة جديدة. | تسمى حدود الفترة والنص والصحة صراحة؛ لا ينسب نجاح نموذج الأعداد إلى قبول بقية المرشحات.<br>**not-executed** |
| P7B27T-28<br>FE7B27-14 / H7B27-05 | فشل المرشح النصي<br>بعد توريد عقد DataView والثقافة، قارن نصاً غير صالح بلقطة قديمة في بيئة معزولة مأذونة. | تظهر حالة failed/dirty دون خلطها بحقن SQL أو إعادة عد P7-074 أو اعتماد جميع المرشحات.<br>**not-executed** |
| P7B27T-29<br>FE7B27-15 / P7-157 | الاستعلام المقيد كمرجع مقارنة<br>قارن شروط أول تنقل بشروط رجوع البحث، من حيث النوع والعملية والفرع. | تعلن الفروق المقصودة بعقد؛ لا يسقط قيد النوع من نتيجة البحث بلا تفسير.<br>**not-executed** |
| P7B27T-30<br>FE7B27-15 / P7-157 | فصل مقارنة المصدر عن الإصلاح<br>افصل المقارنة النصية عن مقترح مجموعة الأنواع عند المستهلك؛ لا تنفيذ أو تجربة SQL في هذا التدقيق. | يبقى كود التطبيق ثابتاً، والخطة غير منفذة، ولرفض النوع غير المسموح معيار واضح.<br>**not-executed** |
| P7B27T-31<br>FE7B27-16 / P7-156;P7-157 | تعيين النوع من المصدر<br>ورد صف 20 بكل الأعمدة المطلوبة في عقد القارئ، ثم تتبع مصدر تعيين InvoiceType و InvoiceStatus. | لا يعلن المستهلك تحميل مشتريات 1 لمجرد صحة GlobalID عندما يسند القارئ النوع 20.<br>**not-executed** |
| P7B27T-32<br>FE7B27-16 / P7-156;P7-157 | عقد النوع والسياق الخارجي<br>ورد manifest و DTO والأعمدة المطلوبة وعقد تحميل مستند موجود قبل اعتماد نموذج التحرير المعروض. | تبقى defaults الخارجية و Loaded في P7-132 عقدين مستقلين؛ لا ترقية 132 إلى confirmed.<br>**not-executed** |
| P7B27T-33<br>FE7B27-17 / P4-014;P7-132;P7-145;P4-020;P4-021 | السجل والحواجز المحفوظة<br>قارن حقول 326 قاموساً و ALLnext_phase و evidence والبادئة الخام و G223 و 765 مادة و 827 أصلاً والتجميدات الثلاثة. | الجديد 155/156/157 فقط؛ لا extensions أو ترقية potential أو دمج إصلاحات.<br>**not-executed** |
| P7B27T-34<br>FE7B27-17 / P4-014;P7-132;P7-145;P4-020;P4-021 | أنساب البقايا والتقسيمات<br>قارن upstream ID و row SHA والعقود والمدخل السابق كاملاً وكل مسار مقابل وتصرف محدد. | تحفظ الأنساب والمدخلات والمسارات كاملة، وتظل كل خطط القبول not-executed.<br>**not-executed** |
| P7B27T-35<br>FE7B27-18 / H7B27-06 | كل 48 حالة B26 بمدخلاتها الأصلية<br>خطة متكاملة بعد إذن مستقل: شغل الطفل presetB26/OWN326/raw327CRLF/indexes و A محلياً، وافحص CLI B27 و API15، ثم بوابات العقود التي لم تنفذ. | تنفذ كل 48 حالة بلا تعديل أو تخط أو تصفية أو global Path أو shared subprocess mutation أو disk overlay أو rebaseline؛ نجاح checker وحده لا ينفذ كامل الخطة.<br>**not-executed** |
| P7B27T-36<br>FE7B27-18 / H7B27-06 | هوية الالتقاط والتسليم للمسار المستقل<br>راجع المصدر 10ba والتقاط B26 عند dd38f97 وتسليمه 6eedc06، ثم قدم SHA تدقيق مدفوعاً للمحادثة المستقلة. | لا يعاد توليد stdout بعد الدفع، ولا يفترض بدء الإصلاح أو تزامنه؛7B/7 جزئيتان و 7C لم تبدأ و 8 غير مأذونة.<br>**not-executed** |

## 6. الحفظ والإذن والتوازي

765 محمية وكل 326 قاموساًبكلحقل/ALLnext_phase/evidence/raw327CRLFprefix/noBOM/G223/827 أصلاً/29,128,444 بايت/التجميدات الثلاثة. الحالي 329/raw330CRLF و 155/156/157 فقط، وصفر extensions؛G224–228 توصيات غير منفذة لا خمس نتائج أخرى. لا إعادة كتابة أرشيف أو  stdout بعد الدفع،ولا تطابق مصطنع لهوية  capture معالتسليم.

014/132/145 تبقى potential، و 020/021 وحواجز المال والتفويض و ACL والمخزون والحفظ والإنتاج لم تعتمد أو تعالج. تصحيح B10 الإضافي باقٍ:10 محلياً مقابل 120 مرجعياً، وعند equality1 كلاهما 10، مع حفظ G138. لا ERP/build/C#/VB/.NET/WPF/DataView/SQL/provider/SDK/ToDataTable/REPX أو طابعة/ماسح أو بيانات أعمال وأسرار أو إصلاح وقياس وقبول نُفذ هنا.

كل 36 خطة B27 و 32 خطة B26 **غير منفذة**؛ **7B/7 جزئيتان؛R4k محدود؛R4l/7B28 مقترح؛7C لم تبدأ؛8 غير مأذونة هنا**. يسلم SHA تدقيقمدفوعاًلمسار الإصلاح المستقل دون افتراض بدئه أو تزامنه أو دمج تعديلاته هنا.
