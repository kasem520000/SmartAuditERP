using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

namespace zkemkeeper
{
	[ComImport]
	[CompilerGenerated]
	[Guid("102F4206-E43D-4FC9-BAB0-331CFFE4D25B")]
	[TypeIdentifier]
	public interface IZKEM
	{
		void _VtblGap1_8();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(7)]
		bool ReadGeneralLogData([In] int dwMachineNumber);

		void _VtblGap2_2();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(10)]
		bool EnableDevice([In] int dwMachineNumber, [In] bool bFlag);

		void _VtblGap3_7();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(18)]
		void GetLastError([In][Out] ref int dwErrorCode);

		void _VtblGap4_3();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(22)]
		bool GetGeneralLogData([In] int dwMachineNumber, [In][Out] ref int dwTMachineNumber, [In][Out] ref int dwEnrollNumber, [In][Out] ref int dwEMachineNumber, [In][Out] ref int dwVerifyMode, [In][Out] ref int dwInOutMode, [In][Out] ref int dwYear, [In][Out] ref int dwMonth, [In][Out] ref int dwDay, [In][Out] ref int dwHour, [In][Out] ref int dwMinute);

		void _VtblGap5_12();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(36)]
		bool ClearGLog([In] int dwMachineNumber);

		void _VtblGap6_2();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(39)]
		bool Connect_Net([In][MarshalAs(UnmanagedType.BStr)] string IPAdd, [In] int Port);

		void _VtblGap7_9();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(49)]
		bool RefreshData([In] int dwMachineNumber);

		void _VtblGap8_123();

		[MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
		[DispId(171)]
		bool RegEvent([In] int dwMachineNumber, [In] int EventMask);
	}
}